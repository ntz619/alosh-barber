from pathlib import Path
import re

script_path = Path('script.js')
styles_path = Path('styles.css')

js = script_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')

new_func = r'''    // cuts-horizontal-carousel-v4
    function setupCutsCarousel() {
      const track = document.querySelector('[data-cuts-carousel]');
      if (!track) return;

      const originals = [...track.children];
      if (!originals.length) return;

      const createClone = card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        clone.classList.add('in-view');
        clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
        return clone;
      };

      // Keep a complete duplicate on both sides of the real cards. The user can
      // therefore move through the seam in either direction without ever seeing
      // the carousel run out of content.
      const leftCopies = document.createDocumentFragment();
      originals.forEach(card => leftCopies.appendChild(createClone(card)));
      track.prepend(leftCopies);

      const rightCopies = document.createDocumentFragment();
      originals.forEach(card => rightCopies.appendChild(createClone(card)));
      track.append(rightCopies);

      const originalCount = originals.length;
      const originalStart = originalCount;
      const originalEnd = originalStart + originalCount - 1;
      const AUTO_DELAY = 3200;
      const RESUME_DELAY = 3600;
      const SCROLL_DURATION = 800;
      const MANUAL_SETTLE_DELAY = 180;

      let autoTimer = null;
      let settleTimer = null;
      let manualSettleTimer = null;
      let isDragging = false;
      let autoAnimating = false;
      let loopJumping = false;
      let dragStartX = 0;
      let dragStartScrollLeft = 0;
      let setWidth = 0;

      const cards = () => [...track.children];

      const centeredLeft = card => card.offsetLeft - (track.clientWidth - card.offsetWidth) / 2;

      const updateSetWidth = () => {
        const leftFirst = track.children[0];
        const middleFirst = track.children[originalStart];
        setWidth = leftFirst && middleFirst
          ? middleFirst.offsetLeft - leftFirst.offsetLeft
          : track.scrollWidth / 3;
      };

      const nearestCardIndex = () => {
        const center = track.scrollLeft + track.clientWidth / 2;
        const list = cards();
        let nearest = 0;
        let distance = Infinity;

        list.forEach((card, index) => {
          const cardCenter = card.offsetLeft + card.offsetWidth / 2;
          const currentDistance = Math.abs(cardCenter - center);
          if (currentDistance < distance) {
            distance = currentDistance;
            nearest = index;
          }
        });

        return nearest;
      };

      const jumpBySet = delta => {
        if (!delta || !setWidth) return;
        loopJumping = true;
        track.classList.add('is-loop-jump');
        track.scrollLeft += delta;
        requestAnimationFrame(() => {
          track.classList.remove('is-loop-jump');
          loopJumping = false;
        });
      };

      // Move a side duplicate back to the identical card in the middle set. The
      // visual content and its exact viewport position do not change, so the loop
      // is continuous even though the underlying scroll coordinate is recycled.
      const normalizeToMiddle = () => {
        if (!setWidth) return nearestCardIndex();
        const index = nearestCardIndex();

        if (index < originalStart) {
          jumpBySet(setWidth);
          return index + originalCount;
        }

        if (index > originalEnd) {
          jumpBySet(-setWidth);
          return index - originalCount;
        }

        return index;
      };

      const clearAuto = () => {
        if (autoTimer) clearTimeout(autoTimer);
        autoTimer = null;
      };

      const clearSettle = () => {
        if (settleTimer) clearTimeout(settleTimer);
        settleTimer = null;
      };

      const scheduleAuto = (delay = AUTO_DELAY) => {
        clearAuto();
        if (reducedMotion) return;
        autoTimer = setTimeout(advance, delay);
      };

      const beginManualInteraction = () => {
        autoAnimating = false;
        clearAuto();
        clearSettle();
      };

      const scheduleResumeAfterManualScroll = () => {
        if (manualSettleTimer) clearTimeout(manualSettleTimer);
        manualSettleTimer = setTimeout(() => {
          updateSetWidth();
          normalizeToMiddle();
          scheduleAuto(RESUME_DELAY);
        }, MANUAL_SETTLE_DELAY);
      };

      function advance() {
        if (isDragging || document.visibilityState !== 'visible') {
          scheduleAuto(900);
          return;
        }

        updateSetWidth();
        const current = normalizeToMiddle();
        const target = track.children[current + 1];

        if (!target) {
          scheduleAuto();
          return;
        }

        autoAnimating = true;
        track.scrollTo({ left: centeredLeft(target), behavior: 'smooth' });

        clearSettle();
        settleTimer = setTimeout(() => {
          autoAnimating = false;
          normalizeToMiddle();
          scheduleAuto();
        }, SCROLL_DURATION);
      }

      // Any native swipe, touchpad or mouse-wheel movement pauses autoplay. Once
      // the user stops, autoplay resumes from that exact logical card/position.
      track.addEventListener('scroll', () => {
        if (autoAnimating || loopJumping || isDragging) return;
        clearAuto();
        scheduleResumeAfterManualScroll();
      }, { passive: true });

      track.addEventListener('touchstart', beginManualInteraction, { passive: true });
      track.addEventListener('wheel', beginManualInteraction, { passive: true });
      track.addEventListener('focusin', beginManualInteraction, { passive: true });

      track.addEventListener('keydown', event => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        beginManualInteraction();
        updateSetWidth();
        const current = normalizeToMiddle();
        const direction = event.key === 'ArrowRight' ? 1 : -1;
        const target = track.children[current + direction];
        if (target) {
          track.scrollTo({
            left: centeredLeft(target),
            behavior: reducedMotion ? 'auto' : 'smooth'
          });
        }
        scheduleResumeAfterManualScroll();
      });

      track.addEventListener('pointerdown', event => {
        if (event.pointerType !== 'mouse' || event.button !== 0) return;
        beginManualInteraction();
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
        scheduleResumeAfterManualScroll();
      };

      track.addEventListener('pointerup', stopDragging);
      track.addEventListener('pointercancel', stopDragging);
      track.addEventListener('lostpointercapture', stopDragging);

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') scheduleAuto(900);
        else {
          beginManualInteraction();
          if (manualSettleTimer) clearTimeout(manualSettleTimer);
        }
      });

      window.addEventListener('resize', () => {
        beginManualInteraction();
        requestAnimationFrame(() => {
          updateSetWidth();
          normalizeToMiddle();
          scheduleAuto(900);
        });
      });

      requestAnimationFrame(() => {
        updateSetWidth();
        loopJumping = true;
        track.classList.add('is-loop-jump');
        track.scrollLeft = centeredLeft(track.children[originalStart]);
        requestAnimationFrame(() => {
          track.classList.remove('is-loop-jump');
          loopJumping = false;
          scheduleAuto(1200);
        });
      });
    }

    setupCutsCarousel();'''

pattern = r"\s*// cuts-horizontal-carousel-v3\n\s*function setupCutsCarousel\(\) \{.*?\n\s*setupCutsCarousel\(\);"
js, count = re.subn(pattern, '\n\n' + new_func, js, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f'Expected one v3 carousel block, found {count}')

css = css.replace('scroll-snap-type:x mandatory', 'scroll-snap-type:x proximity')
css = css.replace(
    '.cuts-track.is-dragging{cursor:grabbing;scroll-snap-type:none;user-select:none}',
    '.cuts-track.is-dragging{cursor:grabbing;scroll-snap-type:none;user-select:none}\n    .cuts-track.is-loop-jump{scroll-snap-type:none}'
)

script_path.write_text(js, encoding='utf-8')
styles_path.write_text(css, encoding='utf-8')
