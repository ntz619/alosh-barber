from pathlib import Path

for filename in ('index.html', 'impressum.html'):
    path = Path(filename)
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    text = text.replace('href="styles.css"', 'href="styles.css?v=20260819-light4"')
    text = text.replace('href="styles.css?v=20260819-light3"', 'href="styles.css?v=20260819-light4"')
    text = text.replace('href="styles.css?v=20260819-light2"', 'href="styles.css?v=20260819-light4"')
    path.write_text(text, encoding='utf-8')

css_path = Path('styles.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Force light price surface v4 */'
if marker not in css:
    css += r'''

/* Force light price surface v4 */
#services .price-panel-inner,
#services .price-side{
  background:#f3ecdf !important;
  color:#171511 !important;
}
#services .price-intro{
  background:linear-gradient(160deg,#f8f3eb 0%,#eadfce 100%) !important;
  color:#171511 !important;
  border-color:rgba(23,21,17,.10) !important;
}
#services .price-intro h2{color:#171511 !important}
#services .price-kicker{color:#8f6732 !important}
#services .price-category h3{color:#755027 !important}
#services .price-category-note,
#services .price-service,
#services .price-simple-row,
#services .price-simple-row>span{color:#3f3a33 !important}
#services .price-simple-row>strong,
#services .price-cell strong,
#services .price-length-head strong{color:#8a6030 !important}
#services .price-category,
#services .price-length-head,
#services .price-length-row,
#services .price-simple-row{border-color:rgba(23,21,17,.10) !important}
#services .price-info{
  background:rgba(224,192,136,.18) !important;
  color:#5f513e !important;
  border-color:rgba(143,103,50,.22) !important;
}
#services .free-extra-grid span{
  background:rgba(255,255,255,.58) !important;
  color:#4c4338 !important;
  border-color:rgba(143,103,50,.20) !important;
}

@media(max-width:780px){
  #services [data-gender-panel="damen"] .price-length-row,
  #services [data-gender-panel="damen"] .price-simple-in-table{
    background:#fffaf3 !important;
    border-color:rgba(23,21,17,.10) !important;
  }
  #services [data-gender-panel="damen"] .price-cell{
    border-color:rgba(23,21,17,.08) !important;
  }
  #services [data-gender-panel="damen"] .price-cell small{color:#74695d !important}
  #services [data-gender-panel="damen"] .price-service{color:#2f2a24 !important}
}
'''
    css_path.write_text(css, encoding='utf-8')
