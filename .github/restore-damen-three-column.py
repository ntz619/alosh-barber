from pathlib import Path

css_path = Path('styles.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Damen mobile three-column restore v5 */'
if marker not in css:
    css += r'''

/* Damen mobile three-column restore v5 */
@media(max-width:780px){
  #services [data-gender-panel="damen"] .price-length-row{
    display:grid !important;
    grid-template-columns:repeat(3,minmax(0,1fr)) !important;
    gap:8px !important;
    margin:0 !important;
    padding:16px 0 !important;
    border:0 !important;
    border-bottom:1px solid rgba(23,21,17,.10) !important;
    border-radius:0 !important;
    background:transparent !important;
  }
  #services [data-gender-panel="damen"] .price-service{
    grid-column:1/-1 !important;
    display:block !important;
    margin:0 0 4px !important;
    color:#2f2a24 !important;
    font-size:20px !important;
    font-weight:700 !important;
    line-height:1.28 !important;
  }
  #services [data-gender-panel="damen"] .price-cell{
    display:flex !important;
    flex-direction:column !important;
    align-items:flex-start !important;
    justify-content:flex-start !important;
    min-width:0 !important;
    width:auto !important;
    padding:11px 10px !important;
    text-align:left !important;
    border:1px solid rgba(143,103,50,.12) !important;
    border-radius:12px !important;
    background:#fffaf3 !important;
  }
  #services [data-gender-panel="damen"] .price-cell small{
    display:block !important;
    margin:0 0 5px !important;
    color:#74695d !important;
    font-size:14px !important;
    font-weight:700 !important;
    line-height:1.15 !important;
  }
  #services [data-gender-panel="damen"] .price-cell strong{
    color:#835b2d !important;
    font-size:18px !important;
    line-height:1.15 !important;
    white-space:nowrap !important;
  }
  #services [data-gender-panel="damen"] .price-simple-in-table{
    margin:0 !important;
    padding:15px 0 !important;
    border:0 !important;
    border-bottom:1px solid rgba(23,21,17,.10) !important;
    border-radius:0 !important;
    background:transparent !important;
  }
}

@media(max-width:390px){
  #services [data-gender-panel="damen"] .price-length-row{gap:6px !important}
  #services [data-gender-panel="damen"] .price-service{font-size:19px !important}
  #services [data-gender-panel="damen"] .price-cell{padding:10px 7px !important}
  #services [data-gender-panel="damen"] .price-cell small{font-size:13px !important}
  #services [data-gender-panel="damen"] .price-cell strong{font-size:16px !important}
}
'''
    css_path.write_text(css, encoding='utf-8')

index_path = Path('index.html')
html = index_path.read_text(encoding='utf-8')
html = html.replace('styles.css?v=20260819-light4', 'styles.css?v=20260819-damen-columns5')
html = html.replace('href="styles.css"', 'href="styles.css?v=20260819-damen-columns5"')
index_path.write_text(html, encoding='utf-8')
