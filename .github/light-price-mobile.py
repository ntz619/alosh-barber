from pathlib import Path

path = Path('styles.css')
css = path.read_text(encoding='utf-8')
marker = '/* Light price lists v3 */'
if marker in css:
    raise SystemExit('Light price list styles already present')

css += r'''

/* Light price lists v3 */
#services .price-panel-inner{
  background:#f3ecdf;
  color:var(--ink);
  border-color:rgba(23,21,17,.10);
}
#services .price-intro{
  background:linear-gradient(160deg,#f7f1e8 0%,#eadfce 100%);
  border-right:1px solid rgba(23,21,17,.10);
}
#services .price-intro .scroll-decor{color:rgba(112,78,35,.08)}
#services .price-kicker{color:#8f6732!important}
#services .price-intro h2{color:var(--ink)}
#services .price-side{background:#f3ecdf}
#services .price-category{border-top-color:rgba(23,21,17,.12)}
#services .price-category h3{color:#755027}
#services .price-category-note{color:#6f655a}
#services .price-simple-row{border-bottom-color:rgba(23,21,17,.09);color:#2f2b26}
#services .price-simple-row>span{color:#3f3a33}
#services .price-simple-row>strong{color:#8a6030}
#services .price-length-head{border-bottom-color:rgba(23,21,17,.12)}
#services .price-length-head strong{color:#8a6030}
#services .price-length-head small{color:#796f63}
#services .price-length-row{border-bottom-color:rgba(23,21,17,.09)}
#services .price-service{color:#3f3a33}
#services .price-cell strong{color:#8a6030}
#services .price-na strong{color:#9b9388}
#services .free-extra-grid span{
  border-color:rgba(143,103,50,.20);
  background:rgba(255,255,255,.48);
  color:#4c4338;
}
#services .price-info{
  border-color:rgba(143,103,50,.22);
  background:rgba(224,192,136,.18);
  color:#5f513e;
}

@media(max-width:1100px){
  #services .price-intro{border-bottom-color:rgba(23,21,17,.10)}
}

@media(max-width:780px){
  #services .price-side{
    background:#f3ecdf;
    padding:8px 16px 108px;
  }
  #services .price-category,
  #services .price-category:nth-child(-n+2){
    border-top-color:rgba(23,21,17,.12);
  }

  /* Damen: keep large text, but make each service a clear readable block. */
  #services [data-gender-panel="damen"] .length-category{
    padding-top:26px;
  }
  #services [data-gender-panel="damen"] .price-length-row{
    display:block;
    margin:10px 0;
    padding:14px 15px 10px;
    border:1px solid rgba(23,21,17,.09);
    border-radius:16px;
    background:rgba(255,255,255,.54);
  }
  #services [data-gender-panel="damen"] .price-length-row:last-child{
    border-bottom:1px solid rgba(23,21,17,.09);
  }
  #services [data-gender-panel="damen"] .price-service{
    display:block;
    margin:0 0 10px;
    color:#2f2a24;
    font-size:20px;
    font-weight:700;
    line-height:1.28;
  }
  #services [data-gender-panel="damen"] .price-cell{
    display:grid;
    grid-template-columns:minmax(0,1fr) auto;
    align-items:center;
    gap:16px;
    width:100%;
    padding:10px 0;
    text-align:left;
    border-top:1px solid rgba(23,21,17,.08);
  }
  #services [data-gender-panel="damen"] .price-cell:first-of-type{border-top:0}
  #services [data-gender-panel="damen"] .price-cell small{
    display:block;
    color:#74695d;
    font-size:16px;
    font-weight:650;
  }
  #services [data-gender-panel="damen"] .price-cell strong{
    color:#835b2d;
    font-size:19px;
    white-space:nowrap;
  }
  #services [data-gender-panel="damen"] .price-simple-in-table{
    margin:10px 0;
    padding:14px 15px;
    border:1px solid rgba(23,21,17,.09);
    border-radius:16px;
    background:rgba(255,255,255,.54);
  }

  /* Herren uses the same light hierarchy without unnecessary card clutter. */
  #services [data-gender-panel="herren"] .price-simple-row{color:#2f2b26}
  #services .free-extra-grid span{background:rgba(255,255,255,.58)}
}

@media(max-width:390px){
  #services .price-side{padding-inline:13px}
  #services [data-gender-panel="damen"] .price-length-row{padding:13px 13px 9px}
  #services [data-gender-panel="damen"] .price-service{font-size:19px}
  #services [data-gender-panel="damen"] .price-cell small{font-size:15px}
  #services [data-gender-panel="damen"] .price-cell strong{font-size:18px}
}
'''

path.write_text(css, encoding='utf-8')
