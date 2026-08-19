from pathlib import Path
import re

index_path = Path('index.html')
styles_path = Path('styles.css')
script_path = Path('script.js')

html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')
js = script_path.read_text(encoding='utf-8')

services = r'''      <section class="stack-panel price-panel" id="services" style="--z:10">
        <div class="panel-inner cream price-panel-inner">
          <div class="panel-grid price-layout">
            <div class="panel-copy cream-copy price-intro reveal reveal-left">
              <div class="scroll-decor parallax" data-speed="0.12">PREISE</div>
              <p class="price-kicker">Preisliste</p>
              <h2>Damen &amp;<br>Herren.</h2>
              <p>Wähle unten zwischen Damen und Herren. Die komplette Preisliste wechselt direkt mit deiner Auswahl.</p>
            </div>

            <div class="price-side gender-panel" data-gender-panel="herren">
              <section class="price-category">
                <div class="price-category-head"><span>01</span><h3>Haare &amp; Styling</h3></div>
                <div class="price-simple-row"><span>Trockenhaarschnitt + Styling</span><strong>21 €</strong></div>
                <div class="price-simple-row"><span>Haarschnitt mit Maschine, gleiche Länge</span><strong>10 €</strong></div>
                <div class="price-simple-row"><span>Waschen</span><strong>2 €</strong></div>
              </section>

              <section class="price-category">
                <div class="price-category-head"><span>02</span><h3>Bart</h3></div>
                <div class="price-simple-row"><span>Haarschnitt mit Bart</span><strong>35 €</strong></div>
                <div class="price-simple-row"><span>Bartrasur</span><strong>14 €</strong></div>
              </section>

              <section class="price-category">
                <div class="price-category-head"><span>03</span><h3>Kosmetik</h3></div>
                <div class="price-simple-row"><span>Augenbrauen zupfen</span><strong>5 €</strong></div>
              </section>

              <section class="price-category">
                <div class="price-category-head"><span>04</span><h3>Kinder</h3></div>
                <div class="price-simple-row"><span>Bis 10 Jahre</span><strong>12 €</strong></div>
                <div class="price-simple-row"><span>Ab 10 Jahre</span><strong>21 €</strong></div>
              </section>

              <section class="price-category price-category-wide price-extras">
                <div class="price-category-head"><span>+</span><h3>Kostenlose Extras</h3></div>
                <div class="free-extra-grid">
                  <span>Ohren + Nase<br>mit Wachs</span>
                  <span>Haarmaske</span>
                  <span>Gesichtsmaske</span>
                </div>
              </section>
            </div>

            <div class="price-side gender-panel" data-gender-panel="damen" hidden>
              <section class="price-category price-category-wide length-category">
                <div class="price-category-head"><span>01</span><h3>Schnitt &amp; Styling</h3></div>
                <div class="price-length-head" aria-hidden="true">
                  <span></span><strong>Kurz<small>bis Kinn</small></strong><strong>Mittel<small>bis Schulter</small></strong><strong>Lang<small>ab Schulter</small></strong>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Waschen · Schneiden · Föhnen</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 45 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>55 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>65 €</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Waschen · Schneiden</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 35 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>45 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>55 €</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Waschen · Föhnen</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 28 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>35 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>45 €</strong></span>
                </div>
                <div class="price-simple-row price-simple-in-table"><span>Ponyschnitt</span><strong>10 €</strong></div>
                <div class="price-length-row">
                  <span class="price-service">Haare glätten</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 29 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>39 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>49 €</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Haare locken</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 30 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>40 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>50 €</strong></span>
                </div>
              </section>

              <section class="price-category price-category-wide length-category">
                <div class="price-category-head"><span>02</span><h3>Farbe</h3></div>
                <div class="price-length-head" aria-hidden="true">
                  <span></span><strong>Kurz<small>bis Kinn</small></strong><strong>Mittel<small>bis Schulter</small></strong><strong>Lang<small>ab Schulter</small></strong>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Farbe komplett</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 60 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>75 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>85 €</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Ansatzfärbung (bis 2 cm)</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 50 €</strong></span>
                  <span class="price-cell price-na"><small>Mittel</small><strong>–</strong></span>
                  <span class="price-cell price-na"><small>Lang</small><strong>–</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Ansatztönung (mehr als 2 cm)</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 60 €</strong></span>
                  <span class="price-cell price-na"><small>Mittel</small><strong>–</strong></span>
                  <span class="price-cell price-na"><small>Lang</small><strong>–</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Tönung</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 40 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>48 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>55 €</strong></span>
                </div>
              </section>

              <section class="price-category price-category-wide length-category">
                <div class="price-category-head"><span>03</span><h3>Blond &amp; Highlights</h3></div>
                <div class="price-length-head" aria-hidden="true">
                  <span></span><strong>Kurz<small>bis Kinn</small></strong><strong>Mittel<small>bis Schulter</small></strong><strong>Lang<small>ab Schulter</small></strong>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Balayage</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 75 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>90 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>110 €</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Strähnen</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 70 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>80 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>100 €</strong></span>
                </div>
              </section>

              <section class="price-category price-category-wide length-category">
                <div class="price-category-head"><span>04</span><h3>Glättung &amp; Umformung</h3></div>
                <div class="price-length-head" aria-hidden="true">
                  <span></span><strong>Kurz<small>bis Kinn</small></strong><strong>Mittel<small>bis Schulter</small></strong><strong>Lang<small>ab Schulter</small></strong>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Keratinglättung</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 130 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>160 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>190 €</strong></span>
                </div>
                <div class="price-length-row">
                  <span class="price-service">Dauerwelle</span>
                  <span class="price-cell"><small>Kurz</small><strong>ab 60 €</strong></span>
                  <span class="price-cell"><small>Mittel</small><strong>70 €</strong></span>
                  <span class="price-cell"><small>Lang</small><strong>80 €</strong></span>
                </div>
              </section>

              <section class="price-category">
                <div class="price-category-head"><span>05</span><h3>Pflege</h3></div>
                <div class="price-simple-row"><span>Haarmaske</span><strong>ab 10 €</strong></div>
                <div class="price-simple-row"><span>Intensivkur (Haarmaske + Ampulle)</span><strong>ab 18 €</strong></div>
              </section>

              <section class="price-category">
                <div class="price-category-head"><span>06</span><h3>Kosmetik</h3></div>
                <div class="price-simple-row"><span>Augenbrauen zupfen</span><strong>10 €</strong></div>
                <div class="price-simple-row"><span>Augenbrauen färben</span><strong>10 €</strong></div>
                <div class="price-simple-row"><span>Wimpern färben</span><strong>12 €</strong></div>
              </section>

              <section class="price-category">
                <div class="price-category-head"><span>07</span><h3>Hochzeit &amp; Specials</h3></div>
                <div class="price-simple-row"><span>Hochsteckfrisur</span><strong>ab 65 €</strong></div>
                <div class="price-simple-row"><span>Frisur</span><strong>200 €</strong></div>
                <div class="price-simple-row"><span>Frisur mit Make-up</span><strong>250 €</strong></div>
                <div class="price-simple-row"><span>Probestecken</span><strong>ab 70–100 €</strong></div>
                <div class="price-simple-row"><span>Make-up</span><strong>ab 60 €</strong></div>
              </section>

              <section class="price-category">
                <div class="price-category-head"><span>08</span><h3>Kinder</h3></div>
                <p class="price-category-note">Mädchen bis 12 Jahre</p>
                <div class="price-simple-row"><span>Waschen · Schneiden · Stylen</span><strong>25 €</strong></div>
              </section>

              <aside class="price-info price-category-wide">
                Alle Preise verstehen sich inklusive Beratung, Waschen und hochwertiger Pflegeprodukte.
              </aside>
            </div>
          </div>
        </div>
      </section>'''

html, count = re.subn(
    r'      <section class="stack-panel(?: price-panel)?" id="services".*?</section>\n\n      <section class="stack-panel" id="salon"',
    services + '\n\n      <section class="stack-panel" id="salon"',
    html,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f'Could not replace services section: {count}')

marker = '/* Full mobile-first price lists */'
if marker not in css:
    css += r'''

/* Full mobile-first price lists */
#services.price-panel{position:relative;top:auto;height:auto;margin-bottom:var(--section-space)}
#services .price-panel-inner{height:auto;min-height:0;overflow:hidden}
#services .price-layout{height:auto;grid-template-columns:minmax(260px,.7fr) minmax(0,1.3fr);align-items:start}
#services .price-intro{align-self:start;justify-content:flex-start;padding-top:clamp(38px,5vw,64px)}
.price-kicker{margin:0 0 12px!important;color:#8f6732!important;font-size:16px!important;font-weight:700;text-transform:uppercase;letter-spacing:.16em}
.price-side{min-width:0;padding:clamp(20px,2.6vw,36px);display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;background:rgba(255,255,255,.28)}
.price-category{min-width:0;background:rgba(255,255,255,.72);border:1px solid rgba(23,21,17,.09);border-radius:22px;padding:clamp(20px,2.3vw,28px)}
.price-category-wide{grid-column:1/-1}
.price-category-head{display:flex;align-items:center;gap:13px;padding-bottom:15px;margin-bottom:4px;border-bottom:1px solid rgba(23,21,17,.13)}
.price-category-head>span{display:grid;place-items:center;flex:0 0 38px;width:38px;height:38px;border:1px solid rgba(143,103,50,.36);border-radius:50%;font-size:14px;font-weight:700;color:#8f6732}
.price-category h3{font:500 clamp(28px,3vw,40px)/1 "Cormorant Garamond",serif;color:var(--ink);overflow-wrap:anywhere}
.price-category-note{margin:12px 0 2px;color:#776b5c;font-size:16px;font-weight:600}
.price-simple-row{display:flex;align-items:flex-start;justify-content:space-between;gap:22px;padding:14px 0;border-bottom:1px solid rgba(23,21,17,.09);font-size:18px;line-height:1.32}
.price-simple-row:last-child{border-bottom:0;padding-bottom:0}
.price-simple-row>span{min-width:0;color:#3f3a33}
.price-simple-row>strong{flex:0 0 auto;color:#8a6030;font-size:19px;white-space:nowrap}
.price-simple-in-table{margin-top:0}
.price-length-head,.price-length-row{display:grid;grid-template-columns:minmax(220px,1.5fr) repeat(3,minmax(86px,.55fr));column-gap:12px;align-items:center}
.price-length-head{padding:13px 0 9px;border-bottom:1px solid rgba(23,21,17,.12)}
.price-length-head strong{text-align:center;color:#8f6732;font-size:16px;line-height:1.1}
.price-length-head small{display:block;margin-top:3px;color:#796f63;font-size:12px;font-weight:500}
.price-length-row{padding:13px 0;border-bottom:1px solid rgba(23,21,17,.09)}
.price-length-row:last-child{border-bottom:0}
.price-service{font-size:18px;line-height:1.3;color:#3f3a33;overflow-wrap:anywhere}
.price-cell{text-align:center;min-width:0}
.price-cell small{display:none}
.price-cell strong{color:#8a6030;font-size:18px;white-space:nowrap}
.price-na strong{color:#938b81;font-weight:500}
.free-extra-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;padding-top:18px}
.free-extra-grid span{display:grid;place-items:center;min-height:96px;text-align:center;padding:16px;border:1px solid rgba(143,103,50,.2);border-radius:18px;color:#4c4338;font-size:17px;line-height:1.3;font-weight:600}
.price-info{padding:20px 22px;border:1px solid rgba(143,103,50,.24);border-radius:20px;background:rgba(224,192,136,.16);color:#5f513e;font-size:17px;line-height:1.45}

@media(max-width:1100px){
  #services .price-layout{grid-template-columns:1fr}
  #services .price-intro{padding-bottom:12px}
  .price-side{grid-template-columns:1fr 1fr}
}

@media(max-width:780px){
  #services.price-panel{margin-inline:0}
  #services .price-panel-inner{border-radius:24px}
  #services .price-intro{padding:28px 20px 16px}
  #services .price-intro h2{font-size:clamp(46px,14vw,60px)}
  #services .price-intro p{font-size:19px}
  .price-side{grid-template-columns:1fr;padding:12px 14px 106px;gap:14px;background:rgba(255,255,255,.2)}
  .price-category{grid-column:auto;padding:20px 17px;border-radius:20px}
  .price-category-wide{grid-column:auto}
  .price-category h3{font-size:34px}
  .price-category-head{gap:11px;padding-bottom:13px}
  .price-category-head>span{width:36px;height:36px;flex-basis:36px}
  .price-simple-row{font-size:19px;gap:14px;padding:15px 0}
  .price-simple-row>strong{font-size:19px}
  .price-length-head{display:none}
  .price-length-row{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;padding:16px 0}
  .price-service{grid-column:1/-1;font-size:20px;font-weight:600;margin-bottom:2px}
  .price-cell{display:flex;flex-direction:column;align-items:flex-start;text-align:left;min-width:0;padding:10px 9px;background:rgba(239,232,220,.74);border-radius:12px}
  .price-cell small{display:block;color:#786b5b;font-size:13px;font-weight:700;margin-bottom:4px}
  .price-cell strong{font-size:17px;white-space:normal}
  .price-simple-in-table{margin-top:0}
  .free-extra-grid{grid-template-columns:1fr;gap:9px}
  .free-extra-grid span{min-height:0;display:block;text-align:left;font-size:18px;padding:14px 15px}
  .price-info{font-size:17px;padding:18px}
}

@media(max-width:390px){
  .price-side{padding-inline:10px}
  .price-category{padding:18px 14px}
  .price-category h3{font-size:31px}
  .price-service{font-size:19px}
  .price-cell{padding:9px 7px}
  .price-cell strong{font-size:16px}
  .price-simple-row{font-size:18px}
  .price-simple-row>strong{font-size:18px}
}
'''

# Do not include the tall price panel in the decorative sticky-card scaling logic.
js = js.replace(
    "const stickyPanels = [...document.querySelectorAll('.stack-panel')];",
    "const stickyPanels = [...document.querySelectorAll('.stack-panel:not(.price-panel)')];"
)

index_path.write_text(html, encoding='utf-8')
styles_path.write_text(css, encoding='utf-8')
script_path.write_text(js, encoding='utf-8')
