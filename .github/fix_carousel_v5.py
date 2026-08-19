from pathlib import Path
import re

script_path = Path('script.js')
js = script_path.read_text(encoding='utf-8')

new_func = r'''function setupCutsCarousel() {
  const track = document.querySelector('[data-cuts-carousel]');
  if (!track) return;

  const originals = [...track.children];
  if (!originals.length) return;

  track.style.scrollSnapType = 'none';
  track.style.scrollBehavior = 'auto';
  originals.forEach(card => { card.style.scrollSnapAlign = 'none'; });

  const cloneCard = card => {
    const clone = card.cloneNode(true);
    clone.setAttribute('aria-hidden', 'true');
    clone.classList.add('in-view');
    clone.style.scrollSnapAlign = 'none';
    clone.querySelectorAll('img').forEach(img => img.removeAttribute('loading'));
    return clone;
  };

  // Large repeated buffer: last -> first is always just the next physical card.
  // We only recycle the scroll coordinate several full loops later, while stopped.
  const BUFFER_SETS = 4;
  const leftCopies = document.createDocumentFragment();
  for (let set = 0; set < BUFFER_SETS; set += 1) {
    originals.forEach(card => leftCopies.appendChild(cloneCard(card)));
  }
  track.prepend(leftCopies);

  const rightCopies = document.createDocumentFragment();
  for (let set = 0; set < BUFFER_SETS; set += 1) {
    originals.forEach(card => rightCopies.appendChild(cloneCard(card)));
  }
  track.append(rightCopies);

  const count = originals.length;
  const totalSets = BUFFER_SETS * 2 + 1;
  const middleSet = BUFFER_SETS;
  const middleStart = middleSet * count;
  const AUTO_DELAY = 3200;
  const RESUME_DELAY = 3600;
  const AUTO_DURATION = 720;

  let period = 0;
  let autoTimer = null;
  let manualTimer = null;
  let animationFrame = null;
  let autoAnimating = false;
  let suppressScroll = false;
  let dragging = false;
  let dragStartX = 0;
  let dragStartScrollLeft = 0;

  const cards = () => [...track.children];
  const centeredLeft = card => card.offsetLeft + card.offsetWidth / 2 - track.clientWidth / 2;

  const updatePeriod = () => {
    const first = track.children[middleStart];
    const repeatedFirst = track.children[middleStart + count];
    if (first && repeatedFirst) period = repeatedFirst.offsetLeft - first.offsetLeft;
  };

  const nearestIndex = () => {
    const viewportCenter = track.scrollLeft + track.clientWidth / 2;
    let nearest = middleStart;
    let bestDistance = Infinity;

    cards().forEach((card, index) => {
      const cardCenter = card.offsetLeft + card.offsetWidth / 2;
      const distance = Math.abs(cardCenter - viewportCenter);
      if (distance < bestDistance) {
        bestDistance = distance;
        nearest = index;
      }
    });

    return nearest;
  };

  const jumpBy = amount => {
    if (!amount) return;
    suppressScroll = true;
    track.scrollLeft += amount;
    requestAnimationFrame(() => {
      requestAnimationFrame(() => { suppressScroll = false; });
    });
  };

  const maybeRecenter = () => {
    updatePeriod();
    let index = nearestIndex();
    const setIndex = Math.floor(index / count);

    // Keep two complete untouched sets on both sides. Normal last->first autoplay
    // transitions never call this branch, so there is no seam reset every cycle.
    if (setIndex <= 1 || setIndex >= totalSets - 2) {
      const logicalIndex = index % count;
      const targetIndex = middleStart + logicalIndex;
      const setDelta = middleSet - setIndex;
      jumpBy(setDelta * period);
      index = targetIndex;
    }

    return index;
  };

  const clearAuto = () => {
    if (autoTimer) clearTimeout(autoTimer);
    autoTimer = null;
  };

  const clearManual = () => {
    if (manualTimer) clearTimeout(manualTimer);
    manualTimer = null;
  };

  const cancelAnimation = () => {
    if (animationFrame) cancelAnimationFrame(animationFrame);
    animationFrame = null;
    autoAnimating = false;
  };

  const animateTo = (targetLeft, duration, onDone) => {
    cancelAnimation();
    const startLeft = track.scrollLeft;
    const delta = targetLeft - startLeft;
    const startedAt = performance.now();
    autoAnimating = true;

    const step = now => {
      const progress = Math.min((now - startedAt) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      track.scrollLeft = startLeft + delta * eased;

      if (progress < 1) {
        animationFrame = requestAnimationFrame(step);
        return;
      }

      animationFrame = null;
      autoAnimating = false;
      onDone?.();
    };

    animationFrame = requestAnimationFrame(step);
  };

  const scheduleAuto = (delay = AUTO_DELAY) => {
    clearAuto();
    if (reducedMotion) return;
    autoTimer = setTimeout(advance, delay);
  };

  const beginManualInteraction = () => {
    clearAuto();
    clearManual();
    cancelAnimation();
  };

  const scheduleResume = (autoplayDelay = RESUME_DELAY) => {
    clearManual();
    manualTimer = setTimeout(() => {
      maybeRecenter();
      scheduleAuto(autoplayDelay);
    }, 240);
  };

  function advance() {
    if (dragging || document.visibilityState !== 'visible') {
      scheduleAuto(900);
      return;
    }

    const current = maybeRecenter();
    const target = track.children[current + 1];
    if (!target) {
      maybeRecenter();
      scheduleAuto(500);
      return;
    }

    // No reset here after the last image: the next repeated first image is already
    // physically next in the strip, so the visual motion remains continuous.
    animateTo(centeredLeft(target), AUTO_DURATION, () => scheduleAuto());
  }

  track.addEventListener('scroll', () => {
    if (autoAnimating || suppressScroll || dragging) return;
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

    const current = maybeRecenter();
    const direction = event.key === 'ArrowRight' ? 1 : -1;
    const target = track.children[current + direction];
    if (!target) return;

    animateTo(centeredLeft(target), 560, () => scheduleAuto(RESUME_DELAY));
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
      const current = nearestIndex();
      const logicalIndex = current % count;
      const target = track.children[middleStart + logicalIndex];
      if (target) {
        suppressScroll = true;
        track.scrollLeft = centeredLeft(target);
        requestAnimationFrame(() => { suppressScroll = false; });
      }
      scheduleAuto(1000);
    });
  });

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      updatePeriod();
      const first = track.children[middleStart];
      if (first) {
        suppressScroll = true;
        track.scrollLeft = centeredLeft(first);
        requestAnimationFrame(() => {
          requestAnimationFrame(() => { suppressScroll = false; });
        });
      }
      scheduleAuto(1400);
    });
  });
}

setupCutsCarousel();'''

pattern = r"\s*// cuts-horizontal-carousel-v5\n\s*function setupCutsCarousel\(\) \{.*?\n\s*setupCutsCarousel\(\);"
js, count = re.subn(pattern, '\n\n' + new_func, js, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f'Expected one v5 carousel block, found {count}')

script_path.write_text(js, encoding='utf-8')
