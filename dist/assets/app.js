(() => {
  'use strict';

  // ── 1. КОНСТАНТЫ ─────────────────────────────────────────────────────────

  const PRELOADER_PHRASES = (
    Array.isArray(window.SYNASTRY_PHRASES) && window.SYNASTRY_PHRASES.length >= 3
      ? window.SYNASTRY_PHRASES
      : [
          'Analyzing natal charts...',
          'Mapping Venus and Mars...',
          'Calculating synastry...',
          'Reading karmic nodes...',
          'Checking lunar aspects...',
          'Comparing elements...',
          'Generating your report...',
        ]
  );

  const TIMINGS = {
    sphereInitial:   2000,
    phraseFade:       200,
    phraseVisible:    900,
    pointStagger:     350,
    cliffhangerDelay: 600,
    paywallDelay:       0,
    ctaDelay:         300,
  };

  // ── 2. КЕШИРОВАНИЕ DOM ───────────────────────────────────────────────────

  const elSphereWrap    = document.getElementById('sphere');
  const elSphereInner   = elSphereWrap && elSphereWrap.querySelector('.sphere');
  const elPreloader     = document.getElementById('preloader');
  const elPhrase        = document.getElementById('preloaderPhrase');
  const elResults       = document.getElementById('results');
  const elPoints        = elResults && Array.from(elResults.querySelectorAll('.point'));
  const elCliffhanger   = elResults && elResults.querySelector('.cliffhanger');
  const elPaywall       = document.getElementById('paywall');
  const elCta           = document.getElementById('ctaButton');

  // ── 3. УТИЛИТЫ ───────────────────────────────────────────────────────────

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  const prefersReducedMotion = () =>
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function warn(msg) {
    console.warn(`[synastry] ${msg}`);
  }

  // ── 4. ШАГИ ВОРОНКИ ──────────────────────────────────────────────────────

  async function step1_sphere() {
    if (!elSphereWrap) { warn('sphere not found'); return; }
    if (elSphereInner) elSphereInner.classList.add('sphere--active');
    await sleep(TIMINGS.sphereInitial);
  }

  async function step2_preloader() {
    if (!elPreloader || !elPhrase) { warn('preloader not found'); return; }

    // Сфера затухает
    if (elSphereWrap) elSphereWrap.classList.add('sphere-wrap--fade');

    // Показываем прелоадер
    elPreloader.removeAttribute('hidden');

    for (let i = 0; i < PRELOADER_PHRASES.length; i++) {
      if (i === 0) {
        elPhrase.textContent = PRELOADER_PHRASES[0];
        await sleep(TIMINGS.phraseVisible);
      } else {
        // fade-out
        elPhrase.classList.add('phrase-fade');
        await sleep(TIMINGS.phraseFade);
        elPhrase.textContent = PRELOADER_PHRASES[i];
        // fade-in
        elPhrase.classList.remove('phrase-fade');
        await sleep(TIMINGS.phraseVisible);
      }
    }
  }

  async function step3_revealPoints() {
    if (!elResults || !elPoints || elPoints.length === 0) {
      warn('results/points not found');
      return;
    }

    // Скрываем прелоадер и сферу
    if (elPreloader) elPreloader.setAttribute('hidden', '');
    if (elSphereWrap) elSphereWrap.classList.add('sphere-wrap--hidden');

    // Показываем секцию результатов
    elResults.removeAttribute('hidden');

    // Последовательное появление каждого пункта
    for (let i = 0; i < elPoints.length; i++) {
      await sleep(i === 0 ? 0 : TIMINGS.pointStagger);
      elPoints[i].classList.add('point--visible');
    }

    // Ждём появления последнего пункта
    await sleep(400);
  }

  async function step4_cliffhanger() {
    if (!elCliffhanger) { warn('cliffhanger not found'); return; }
    await sleep(TIMINGS.cliffhangerDelay);
    elCliffhanger.classList.add('cliffhanger--visible');
    await sleep(500);
  }

  async function step5_paywall() {
    if (!elPaywall) { warn('paywall not found'); return; }
    await sleep(TIMINGS.paywallDelay);
    elPaywall.classList.add('paywall--visible');
  }

  async function step6_cta() {
    if (!elCta) { warn('cta button not found'); return; }
    await sleep(TIMINGS.ctaDelay);
    elCta.classList.add('cta-button--visible');
  }

  function step7_bindCTA() {
    if (!elCta) return;
    let isClicked = false;

    elCta.addEventListener('click', (e) => {
      if (isClicked) {
        e.preventDefault();
        return;
      }
      isClicked = true;

      // Опциональный трекинг через dataLayer (GTM/GA4)
      if (typeof window.dataLayer !== 'undefined') {
        const pairId = elCta.href.match(/compat_([^&]+)/)?.[1] ?? 'unknown';
        window.dataLayer.push({ event: 'cta_click', pair_id: pairId });
      }
    });
  }

  // ── 5. МГНОВЕННОЕ КОНЕЧНОЕ СОСТОЯНИЕ (reduced motion) ───────────────────

  function showFinalStateImmediately() {
    if (elSphereWrap) elSphereWrap.classList.add('sphere-wrap--hidden');
    if (elPreloader)  elPreloader.setAttribute('hidden', '');
    if (elResults) {
      elResults.removeAttribute('hidden');
      if (elPoints) elPoints.forEach((p) => p.classList.add('point--visible'));
      if (elCliffhanger) elCliffhanger.classList.add('cliffhanger--visible');
    }
    if (elPaywall) elPaywall.classList.add('paywall--visible');
    if (elCta)    elCta.classList.add('cta-button--visible');
    step7_bindCTA();
  }

  // ── 6. ORCHESTRATOR ──────────────────────────────────────────────────────

  async function runFunnel() {
    if (prefersReducedMotion()) {
      showFinalStateImmediately();
      return;
    }

    try {
      await step1_sphere();
      await step2_preloader();
      await step3_revealPoints();
      await step4_cliffhanger();
      await step5_paywall();
      await step6_cta();
      step7_bindCTA();
    } catch (err) {
      // Если что-то упало — показываем финальное состояние без анимации
      warn(`Funnel error: ${err.message}. Showing final state.`);
      showFinalStateImmediately();
    }
  }

  // ── 7. ENTRY POINT ───────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', runFunnel);

})();
