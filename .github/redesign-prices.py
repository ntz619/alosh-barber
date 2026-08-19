from pathlib import Path

index_path = Path('index.html')
styles_path = Path('styles.css')
script_path = Path('script.js')

html = index_path.read_text(encoding='utf-8')
css = styles_path.read_text(encoding='utf-8')
js = script_path.read_text(encoding='utf-8')

old_intro = '''            <div class="panel-copy cream-copy price-intro reveal reveal-left">
              <div class="scroll-decor parallax" data-speed="0.12">PREISE</div>
              <p class="price-kicker">Preisliste</p>
              <h2>Damen &amp;<br>Herren.</h2>
              <p>Wähle unten zwischen Damen und Herren. Die komplette Preisliste wechselt direkt mit deiner Auswahl.</p>
            </div>'''
new_intro = '''            <div class="panel-copy price-intro reveal reveal-left">
              <div class="scroll-decor parallax" data-speed="0.12">PREISE</div>
              <p class="price-kicker">Preisliste</p>
              <h2 data-gender-price-title>Herren.</h2>
            </div>'''
if old_intro not in html:
    raise SystemExit('Could not find price intro')
html = html.replace(old_intro, new_intro, 1)

# Make the visible heading react to the existing Damen/Herren toggle.
needle = "  const genderWord = document.querySelector('[data-gender-word]');\n"
if needle not in js:
    raise SystemExit('Could not find genderWord line')
if "data-gender-price-title" not in js:
    js = js.replace(needle, needle + "  const priceTitle = document.querySelector('[data-gender-price-title]');\n", 1)

needle2 = "    if (genderWord) genderWord.textContent = gender === 'damen' ? 'DAMEN' : 'HERREN';\n"
if needle2 not in js:
    raise SystemExit('Could not find applyGender heading line')
if "priceTitle.textContent" not in js:
    js = js.replace(needle2, needle2 + "    if (priceTitle) priceTitle.textContent = gender === 'damen' ? 'Damen.' : 'Herren.';\n", 1)

marker = '/* Price list redesign v2 */'
if marker not in css:
    css += r'''

/* Price list redesign v2 */
#services.price-panel{padding:0}
#services .price-panel-inner{
  background:#0c0b0a;
  color:var(--text);
  border-color:rgba(224,192,136,.18);
}
#services .price-layout{
  grid-template-columns:minmax(250px,.52fr) minmax(0,1.48fr);
  gap:0;
}
#services .price-intro{
  position:sticky;
  top:calc(var(--header) + 26px);
  min-height:360px;
  align-self:start;
  justify-content:center;
  padding:clamp(34px,4vw,56px);
  overflow:hidden;
  background:linear-gradient(160deg,#17130f 0%,#0e0c0a 76%);
  border-right:1px solid rgba(224,192,136,.16);
}
#services .price-intro .scroll-decor{color:rgba(224,192,136,.08);left:-5%;bottom:0}
#services .price-kicker{
  margin:0 0 12px!important;
  color:var(--gold-2)!important;
  font-size:15px!important;
  font-weight:700;
  letter-spacing:.18em;
  text-transform:uppercase;
}
#services .price-intro h2{
  color:#f5efe6;
  font-size:clamp(58px,6vw,92px);
  line-height:.9;
}

#services .price-side{
  padding:clamp(28px,3.4vw,52px);
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:0 34px;
  background:#0c0b0a;
}
#services .price-category{
  min-width:0;
  padding:26px 0 22px;
  background:transparent;
  border:0;
  border-radius:0;
  border-top:1px solid rgba(224,192,136,.18);
}
#services .price-category:nth-child(-n+2){border-top:0}
#services .price-category-wide{grid-column:1/-1}
#services .price-category-head{
  display:flex;
  align-items:center;
  gap:14px;
  padding:0 0 17px;
  margin:0;
  border:0;
}
#services .price-category-head>span{
  width:auto;
  height:auto;
  flex:0 0 auto;
  display:block;
  border:0;
  border-radius:0;
  color:var(--gold);
  font-size:13px;
  font-weight:700;
  letter-spacing:.12em;
}
#services .price-category h3{
  color:#e3c89e;
  font:500 clamp(28px,2.6vw,38px)/1 "Cormorant Garamond",serif;
  letter-spacing:.015em;
}
#services .price-category-note{color:#b8aa98;font-size:16px;margin:0 0 8px}

#services .price-simple-row{
  display:grid;
  grid-template-columns:minmax(0,1fr) auto;
  align-items:start;
  gap:22px;
  padding:14px 0;
  border-bottom:1px solid rgba(255,255,255,.075);
  color:#efe8dc;
  font-size:18px;
  line-height:1.35;
}
#services .price-simple-row:last-child{border-bottom:0}
#services .price-simple-row>span{color:#e4d9cc}
#services .price-simple-row>strong{color:var(--gold-2);font-size:19px;white-space:nowrap}

#services .price-length-head,
#services .price-length-row{
  display:grid;
  grid-template-columns:minmax(240px,1.65fr) repeat(3,minmax(90px,.55fr));
  gap:10px;
  align-items:center;
}
#services .price-length-head{
  padding:10px 0 11px;
  border-bottom:1px solid rgba(224,192,136,.18);
}
#services .price-length-head strong{
  color:var(--gold-2);
  text-align:center;
  font-size:15px;
  letter-spacing:.04em;
}
#services .price-length-head small{
  display:block;
  margin-top:4px;
  color:#9f9486;
  font-size:12px;
  font-weight:500;
  letter-spacing:0;
}
#services .price-length-row{
  padding:15px 0;
  border-bottom:1px solid rgba(255,255,255,.075);
}
#services .price-length-row:last-child{border-bottom:0}
#services .price-service{color:#e4d9cc;font-size:18px;line-height:1.35}
#services .price-cell{text-align:center}
#services .price-cell small{display:none}
#services .price-cell strong{color:var(--gold-2);font-size:18px;white-space:nowrap}
#services .price-na strong{color:#776f65}

#services .free-extra-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:12px;
  padding-top:4px;
}
#services .free-extra-grid span{
  min-height:82px;
  display:grid;
  place-items:center;
  text-align:center;
  padding:14px;
  border:1px solid rgba(224,192,136,.2);
  border-radius:16px;
  background:rgba(224,192,136,.045);
  color:#eee1cf;
  font-size:17px;
  line-height:1.3;
}
#services .price-info{
  margin-top:6px;
  padding:18px 20px;
  border:1px solid rgba(224,192,136,.2);
  border-radius:16px;
  background:rgba(224,192,136,.055);
  color:#cdbda6;
  font-size:16px;
  line-height:1.45;
}

@media(max-width:1100px){
  #services .price-layout{grid-template-columns:1fr}
  #services .price-intro{
    position:relative;
    top:auto;
    min-height:0;
    padding:34px 28px 30px;
    border-right:0;
    border-bottom:1px solid rgba(224,192,136,.16);
  }
  #services .price-side{grid-template-columns:1fr 1fr}
}

@media(max-width:780px){
  #services .price-panel-inner{border-radius:24px}
  #services .price-intro{padding:30px 20px 26px}
  #services .price-intro h2{font-size:clamp(54px,17vw,72px)}
  #services .price-kicker{font-size:14px!important;margin-bottom:8px!important}
  #services .price-side{
    grid-template-columns:1fr;
    padding:8px 18px 108px;
    gap:0;
  }
  #services .price-category,
  #services .price-category:nth-child(-n+2){
    grid-column:auto;
    padding:24px 0 20px;
    border-top:1px solid rgba(224,192,136,.18);
  }
  #services .price-category:first-child{border-top:0}
  #services .price-category h3{font-size:34px}
  #services .price-category-head{gap:10px;padding-bottom:14px}
  #services .price-category-head>span{font-size:12px}
  #services .price-simple-row{
    grid-template-columns:minmax(0,1fr) auto;
    gap:16px;
    padding:15px 0;
    font-size:19px;
  }
  #services .price-simple-row>strong{font-size:19px}

  /* Length-based Damen prices become readable stacked rows instead of a cramped table. */
  #services .price-length-head{display:none}
  #services .price-length-row{
    display:block;
    padding:18px 0 16px;
    border-bottom:1px solid rgba(255,255,255,.09);
  }
  #services .price-service{
    display:block;
    margin-bottom:10px;
    color:#f4eadc;
    font-size:20px;
    font-weight:600;
    line-height:1.3;
  }
  #services .price-cell{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    width:100%;
    padding:9px 0;
    text-align:left;
    border-top:1px solid rgba(255,255,255,.055);
  }
  #services .price-cell:first-of-type{border-top:0}
  #services .price-cell small{
    display:block;
    color:#a89b8b;
    font-size:16px;
    font-weight:600;
  }
  #services .price-cell small::after{font-weight:400;color:#746b61}
  #services .price-cell strong{font-size:19px;white-space:nowrap}
  #services .free-extra-grid{grid-template-columns:1fr;gap:8px}
  #services .free-extra-grid span{
    min-height:0;
    display:block;
    text-align:left;
    padding:14px 15px;
    font-size:18px;
  }
  #services .price-info{font-size:17px}
}

@media(max-width:390px){
  #services .price-side{padding-inline:14px}
  #services .price-category h3{font-size:31px}
  #services .price-simple-row{font-size:18px;gap:12px}
  #services .price-simple-row>strong{font-size:18px}
  #services .price-service{font-size:19px}
  #services .price-cell small{font-size:15px}
  #services .price-cell strong{font-size:18px}
}
'''

index_path.write_text(html, encoding='utf-8')
styles_path.write_text(css, encoding='utf-8')
script_path.write_text(js, encoding='utf-8')
