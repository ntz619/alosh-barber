from pathlib import Path
import re

script_path = Path('script.js')
styles_path = Path('styles.css')

js = script_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')

new_func = r'''    // cuts-horizontal-carousel-v5
    function setupCutsCarousel() {
      const track = document.querySelector('[data-cuts-carousel]');
      if (!track) return;

      const originals = [...track.children];
      if (!originals.length) return;

      const cloneCard = card => {
        const clone = card.cloneNode(true);
        clone.setAttribute('aria-hidden', 'true');
        clone.classList.add('in-view');
        clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
        return clone;
      };

      // One full copy on each side gives us a repeating visual strip:
      // [copy] [real cards] [copy]. We always recycle the scroll coordinate only
      // after motion has fully stopped, while the visible pixels are identical.
      const left = document.createDocumentFragment();
      originals.forEach(card => left.appendChild(cloneCard(card)));
      track.prepend(left);

      const right = document.createDocumentFragment();
      originals.forEach(card => right.appendChild(cloneCard(card)));
      track.append(right);

      const count = originals.length;
      const middleStart = count;
      const middleEnd = middleStart + count - 1;
      const AUTO_DELAY = 3200;
      const RESUME_DELAY = 3600;
      const AUTO_DURATION = 720;

      let period = 0;
      let autoTimer = null;
      let manualTimer = null;
      let animationFrame = null;
      let dragging = false;
      let dragStartX = 0;
      let dragStartScrollLeft = 0;
      let programmaticUntil = 0;

      const allCards = () => [...track.children];
      const centeredLeft = card => card.offsetLeft + card.offsetWidth / 2 - track.clientWidth / 2;

      const updatePeriod = () => {
        const leftFirst = track.children[0];
        const middleFirst = track.children[middleStart];
        if (leftFirst && middleFirst) period = middleFirst.offsetLeft - leftFirst.offsetLeft;
      };

      const nearestIndex = () => {
        const viewportCenter = track.scrollLeft + track.clientWidth / 2;
        let nearest = middleStart;
        let best = Infinity;

        allCards().forEach((card, index) => {
          const distance = Math.abs((card.offsetLeft + card.offsetWidth / 2) - viewportCenter);
          if (distance < best) {
            best = distance;
            nearest = index;
          }
        });

        return nearest;
      };

      const markProgrammatic = (ms = 140) => {
        programmaticUntil = performance.now() + ms;
      };

      const jumpBy = amount => {
        if (!amount || !period) return;
        markProgrammatic(180);
        track.scrollLeft += amount;
      };

      const normalizeToMiddle = () => {
        updatePeriod();
        let index = nearestIndex();

        if (index < middleStart) {
          jumpBy(period);
          index += count;
        } else if (index > middleEnd) {
          jumpBy(-period);
          index -= count;
        }

        return index;
      };

      const clearAuto = () => {
        if (autoTimer) clearTimeout(autoTimer);
        autoTimer = null;
      };

      const clearManualTimer = () => {
        if (manualTimer) clearTimeout(manualTimer);
        manualTimer = null;
      };

      const cancelAnimation = () => {
        if (animationFrame) cancelAnimationFrame(animationFrame);
        animationFrame = null;
      };

      const animateTo = (targetLeft, duration, onDone) => {
        cancelAnimation();
        const startLeft = track.scrollLeft;
        const distance = targetLeft - startLeft;
        const startTime = performance.now();

        const tick = now => {
          const progress = Math.min((now - startTime) / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          markProgrammatic(180);
          track.scrollLeft = startLeft + distance * eased;

          if (progress < 1) {
            animationFrame = requestAnimationFrame(tick);
            return;
          }

          animationFrame = null;
          markProgrammatic(180);
          requestAnimationFrame(() => onDone?.());
        };

        animationFrame = requestAnimationFrame(tick);
      };

      const scheduleAuto = (delay = AUTO_DELAY) => {
        clearAuto();
        if (reducedMotion) return;
        autoTimer = setTimeout(advance, delay);
      };

      const beginManualInteraction = () => {
        clearAuto();
        clearManualTimer();
        cancelAnimation();
      };

      const scheduleResume = (delay = RESUME_DELAY) => {
        clearManualTimer();
        manualTimer = setTimeout(() => {
          normalizeToMiddle();
          scheduleAuto(delay);
        }, 220);
      };

      function advance() {
        if (dragging || document.visibilityState !== 'visible') {
          scheduleAuto(900);
          return;
        }

        const current = normalizeToMiddle();
        const targetIndex = current + 1;
        const target = track.children[targetIndex];

        if (!target) {
          scheduleAuto();
          return;
        }

        animateTo(centeredLeft(target), AUTO_DURATION, () => {
          // When the first right-side clone is centered, recycle the coordinate to
          // the real first card. Because both sets are pixel-identical and there is
          // no browser-controlled smooth scroll or scroll snapping, this is invisible.
          if (targetIndex > middleEnd) jumpBy(-period);
          scheduleAuto();
        });
      }

      track.addEventListener('scroll', () => {
        if (performance.now() < programmaticUntil || dragging || animationFrame) return;
        clearAuto();
        scheduleResume();
      }, { passive: true });

      track.addEventListener('touchstart', beginManualInteraction, { passive: true });
      track.addEventListener('touchend', () => scheduleResume(), { passive: true });
      track.addEventListener('wheel', () => {
        beginManualInteraction();
        scheduleResume(2800);
      }, { passive: true });

      track.addEventListener('keydown', event => {
        if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
        event.preventDefault();
        beginManualInteraction();
        const current = normalizeToMiddle();
        const direction = event.key === 'ArrowRight' ? 1 : -1;
        const target = track.children[current + direction];
        if (!target) return;

        animateTo(centeredLeft(target), 560, () => {
          normalizeToMiddle();
          scheduleAuto(RESUME_DELAY);
        });
      });

      track.addEventListener('pointerdown', event => {
        if (event.pointerType !== 'mouse' || event.button !== 0) return;
        beginManualInteraction();
        dragging = true;
        dragStartX = event.clientX;
        dragStartScrollLeft = track.scrollLeft;
        track.classList.add('is-dragging');
        track.setPointerCapture?.(event.pointerId);
      });

      track.addEventListener('pointermove', event => {
        if (!dragging) return;
        track.scrollLeft = dragStartScrollLeft - (event.clientX - dragStartX);
      });

      const stopDragging = event => {
        if (!dragging) return;
        dragging = false;
        track.classList.remove('is-dragging');
        if (event?.pointerId != null && track.hasPointerCapture?.(event.pointerId)) {
          track.releasePointerCapture(event.pointerId);
        }
        scheduleResume();
      };

      track.addEventListener('pointerup', stopDragging);
      track.addEventListener('pointercancel', stopDragging);
      track.addEventListener('lostpointercapture', stopDragging);

      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') scheduleAuto(900);
        else beginManualInteraction();
      });

      window.addEventListener('resize', () => {
        beginManualInteraction();
        requestAnimationFrame(() => {
          updatePeriod();
          const index = normalizeToMiddle();
          const card = track.children[index];
          if (card) {
            markProgrammatic(200);
            track.scrollLeft = centeredLeft(card);
          }
          scheduleAuto(1000);
        });
      });

      // Start on the real first card and center it precisely. Two frames ensure the
      // browser has final card widths before we calculate the initial position.
      requestAnimationFrame(() => requestAnimationFrame(() => {
        updatePeriod();
        const first = track.children[middleStart];
        if (first) {
          markProgrammatic(220);
          track.scrollLeft = centeredLeft(first);
        }
        scheduleAuto(1400);
      }));
    }

    setupCutsCarousel();'''

pattern = r"\s*// cuts-horizontal-carousel-v4\n\s*function setupCutsCarousel\(\) \{.*?\n\s*setupCutsCarousel\(\);"
js, count = re.subn(pattern, '\n\n' + new_func, js, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f'Expected one v4 carousel block, found {count}')

css = css.replace('scroll-snap-type:x proximity', 'scroll-snap-type:none;scroll-behavior:auto')
css = css.replace('scroll-snap-align:center', 'scroll-snap-align:none')
css = css.replace('\n    .cuts-track.is-loop-jump{scroll-snap-type:none}', '')

script_path.write_text(js, encoding='utf-8')
styles_path.write_text(css, encoding='utf-8')
