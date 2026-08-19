from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')

# Scroll snapping was fighting the previous per-frame sub-pixel autoplay.
# Keep snapping for manual interaction, but move one full card at a time for autoplay.
s = s.replace('scroll-snap-type:x proximity;', 'scroll-snap-type:x mandatory;')

start_marker = '    // cuts-horizontal-carousel-v2\n'
end_marker = '    setupCutsCarousel();\n'
start = s.find(start_marker)
end = s.find(end_marker, start)
if start == -1 or end == -1:
    raise SystemExit('Cuts carousel block not found')
end += len(end_marker)

replacement = r'''    // cuts-horizontal-carousel-v3
    function setupCutsCarousel() {
      const track = document.querySelector('[data-cuts-carousel]');
      if (!track) return;

      const originals = [...track.children];
      if (!originals.length) return;

      originals.forEach(card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        clone.classList.add('in-view');
        clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
        track.appendChild(clone);
      });

      const originalCount = originals.length;
      const AUTO_DELAY = 3200;
      const RESUME_DELAY = 3600;
      const SCROLL_DURATION = 750;

      let autoTimer = null;
      let settleTimer = null;
      let isDragging = false;
      let dragStartX = 0;
      let dragStartScrollLeft = 0;
      let loopWidth = 0;

      const cards = () => [...track.children];

      const updateLoopWidth = () => {
        const firstClone = track.children[originalCount];
        loopWidth = firstClone ? firstClone.offsetLeft - track.children[0].offsetLeft : track.scrollWidth / 2;
      };

      const centeredLeft = card => {
        const raw = card.offsetLeft - (track.clientWidth - card.offsetWidth) / 2;
        return Math.max(0, raw);
      };

      const normalizeLoopPosition = () => {
        if (!loopWidth) return;
        while (track.scrollLeft >= loopWidth) track.scrollLeft -= loopWidth;
        while (track.scrollLeft < 0) track.scrollLeft += loopWidth;
      };

      const nearestCardIndex = () => {
        const center = track.scrollLeft + track.clientWidth / 2;
        const list = cards();
        let nearest = 0;
        let distance = Infinity;
        list.forEach((card, index) => {
          const cardCenter = card.offsetLeft + card.offsetWidth / 2;
          const d = Math.abs(cardCenter - center);
          if (d < distance) {
            distance = d;
            nearest = index;
          }
        });
        return nearest;
      };

      const clearAuto = () => {
        if (autoTimer) clearTimeout(autoTimer);
        autoTimer = null;
      };

      const scheduleAuto = (delay = AUTO_DELAY) => {
        clearAuto();
        if (reducedMotion) return;
        autoTimer = setTimeout(advance, delay);
      };

      const pauseForInteraction = (delay = RESUME_DELAY) => {
        clearAuto();
        if (settleTimer) clearTimeout(settleTimer);
        settleTimer = setTimeout(() => {
          normalizeLoopPosition();
          scheduleAuto(500);
        }, delay);
      };

      function advance() {
        if (isDragging || document.visibilityState !== 'visible') {
          scheduleAuto(900);
          return;
        }

        normalizeLoopPosition();
        let current = nearestCardIndex();
        if (current >= originalCount) current -= originalCount;

        // Move to the next original; after the final original we animate to the
        // identical first clone, then invisibly jump back to the real first card.
        const targetIndex = current === originalCount - 1 ? originalCount : current + 1;
        const target = track.children[targetIndex];
        if (!target) {
          scheduleAuto();
          return;
        }

        track.scrollTo({
          left: centeredLeft(target),
          behavior: 'smooth'
        });

        clearTimeout(settleTimer);
        settleTimer = setTimeout(() => {
          if (targetIndex === originalCount) {
            const first = track.children[0];
            track.scrollLeft = centeredLeft(first);
          }
          scheduleAuto();
        }, SCROLL_DURATION);
      }

      // Native swipe/trackpad/manual scrolling always wins. Autoplay resumes from
      // the visitor's new position instead of resetting to the first image.
      track.addEventListener('touchstart', () => pauseForInteraction(), { passive: true });
      track.addEventListener('touchend', () => pauseForInteraction(), { passive: true });
      track.addEventListener('wheel', () => pauseForInteraction(2800), { passive: true });
      track.addEventListener('focusin', () => pauseForInteraction(), { passive: true });

      track.addEventListener('keydown', event => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        pauseForInteraction();
        const list = cards();
        let current = nearestCardIndex();
        if (current >= originalCount) current -= originalCount;
        const direction = event.key === 'ArrowRight' ? 1 : -1;
        const targetIndex = (current + direction + originalCount) % originalCount;
        track.scrollTo({ left: centeredLeft(list[targetIndex]), behavior: reducedMotion ? 'auto' : 'smooth' });
      });

      track.addEventListener('pointerdown', event => {
        if (event.pointerType !== 'mouse' || event.button !== 0) return;
        clearAuto();
        if (settleTimer) clearTimeout(settleTimer);
        isDragging = true;
        dragStartX = event.clientX;
        dragStartScrollLeft = track.scrollLeft;
        track.classList.add('is-dragging');
        track.setPointerCapture?.(event.pointerId);
      });

      track.addEventListener('pointermove', event => {
        if (!isDragging) return;
        track.scrollLeft = dragStartScrollLeft - (event.clientX - dragStartX);
      });

      const stopDragging = event => {
        if (!isDragging) return;
        isDragging = false;
        track.classList.remove('is-dragging');
        if (event?.pointerId != null && track.hasPointerCapture?.(event.pointerId)) {
          track.releasePointerCapture(event.pointerId);
        }
        pauseForInteraction();
      };

      track.addEventListener('pointerup', stopDragging);
      track.addEventListener('pointercancel', stopDragging);
      track.addEventListener('lostpointercapture', stopDragging);

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') scheduleAuto(900);
        else clearAuto();
      });

      window.addEventListener('resize', () => {
        updateLoopWidth();
        normalizeLoopPosition();
      });

      requestAnimationFrame(() => {
        updateLoopWidth();
        scheduleAuto(1200);
      });
    }

    setupCutsCarousel();
'''

s = s[:start] + replacement + s[end:]
path.write_text(s, encoding='utf-8')
