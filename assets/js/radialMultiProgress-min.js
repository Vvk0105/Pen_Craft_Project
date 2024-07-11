!function(t){t.widget("ui.radialMultiProgress",{version:"1.0.0",options:{thickness:10,"font-size":12,"base-color":"#333",space:1,antiAlias:!1,scaleLabel:!1,centerContent:"",responsive:!1,innerFullCircle:!1,data:[]},_create:function(){this._render()},_createCircle:function(t,e,i,n,s,o,a,r,c,h,l){const d=document.createElementNS(t,"circle");return d.setAttribute("cx",e),d.setAttribute("cy",i),d.setAttribute("r",n),d.setAttribute("fill",s),d.setAttribute("stroke",o),d.setAttribute("stroke-width",a),r&&d.setAttribute("transform",r),c&&(d.setAttribute("stroke-dasharray",c),d.setAttribute("stroke-dashoffset",h),l&&(d.style.transition=`stroke-dashoffset ${l.duration} ${l.style}`)),d},_render:function(){const e="http://www.w3.org/2000/svg";let i=50-this.options.thickness;this.element.css("position","relative");const n=document.createElementNS(e,"svg"),s={width:"100%",height:"100%",viewBox:"0 0 100 100"};this.options.antiAlias&&(s["shape-rendering"]="geometricPrecision"),this.options.responsive&&(s.preserveAspectRatio="xMidYMid meet");for(let t in s)n.setAttribute(t,s[t]);const o=[];this.options.data.forEach(((s,a)=>{if(this.options.innerFullCircle&&a===this.options.data.length-1){const o=i,r=this._createCircle(e,"50","50",o.toString(),this.options["base-color"],"none","0");n.appendChild(r);const c=s.range[1]-s.range[0],h=(s.value-s.range[0])/c*100,l=o+(this.options.data.length-(a+1))*this.options.space,d=50-l+2*l*(1-h/100),p=document.createElementNS(e,"mask"),u=t(p).uniqueId();[{element:document.createElementNS(e,"rect"),attributes:{x:0,y:50-o,width:100,height:2*o,fill:"black"}},{element:document.createElementNS(e,"rect"),attributes:{y:d,x:0,width:100,height:2*o*(h/100),fill:"white"}}].forEach((t=>{for(let e in t.attributes)t.element.setAttribute(e,t.attributes[e]);p.appendChild(t.element)})),n.appendChild(p);const f=this._createCircle(e,"50","50",o.toString(),s.color,"none","0");f.setAttribute("mask","url(#"+t(u).attr("id")+")"),n.appendChild(f),i-=this.options.thickness+this.options.space}else{const t=s.range[1]-s.range[0],a=(s.range[1]-s.value)/t,r=2*Math.PI*i,c=(s.startAngle||0)-90,h=r*a,l=this._createCircle(e,"50","50",i.toString(),"none",this.options["base-color"],this.options.thickness.toString(),`rotate(${c} 50 50)`);n.appendChild(l);const d=this._createCircle(e,"50","50",i.toString(),"none",s.color,this.options.thickness.toString(),`rotate(${c} 50 50)`,r,h,s.animation);if(n.appendChild(d),!s.hideLabel){const t=this.options.scaleLabel?this._getScaledFontSize(s.value,this.options["font-size"]):this.options["font-size"];o.push(`<div style="color: ${s.color}; font-size: ${t}px">${s.value}</div>`)}i-=this.options.thickness+this.options.space}})),this.element.append(n,t("<div></div>").css({position:"absolute",top:"50%",left:"50%",transform:"translate(-50%, -50%)","text-align":"center",width:"100%","pointer-events":"none"}).html(`${this.options.centerContent}${o.join("")}`))},_getScaledFontSize:function(e,i){const n=t("<span>").css({visibility:"hidden",fontSize:i+"px"}).text(e).appendTo(document.body),s=n.width();n.remove();const o=100-(this.options.data.length*this.options.thickness+(this.options.data.length-1)*this.options.space);return s>o?i*(o/s):i},updateValue:function(e,i){const n="number"==typeof e?e:this.options.data.findIndex((t=>t.id===e));if(-1!==n){const e=this.options.data[n];e.value=i;const s=e.range[1]-e.range[0],o=(e.value-e.range[0])/s,a=100*o;let r=50-this.options.thickness;for(let t=0;t<this.options.data.length-1;t++)r-=this.options.thickness+this.options.space;if(this.options.innerFullCircle&&n===this.options.data.length-1){const i=50-r+2*r*(1-a/100),n=t(this.element).find("svg > mask")[0],s=t(n).find("rect")[1];e.animation?t(s).css("transition",`y ${e.animation.duration} ${e.animation.style}, height ${e.animation.duration} ${e.animation.style}`):t(s).css("transition",""),s.setAttribute("y",i),s.setAttribute("height",2*r*(a/100))}else{const i=50-this.options.thickness*(n+1)-this.options.space*n,s=2*Math.PI*i*(1-o),a=t(this.element).find("svg > circle")[2*n+1];t(a).attr("stroke-dashoffset",s),e.animation&&t(a).css("transition",`stroke-dashoffset ${e.animation.duration} ${e.animation.style}`)}const c=t(this.element).find("div > div")[n],h=e.hideLabel?"":i;t(c).text(h)}},setAnimation:function(t,e){const i="number"==typeof t?t:this.options.data.findIndex((e=>e.id===t));if(-1!==i){const t=this.options.data[i];t.animation=e;const n=this.element.find("svg > circle");if(n.length>2*i+1){const e=n[2*i+1];t.animation&&(e.style.transition=`stroke-dashoffset ${t.animation.duration} ${t.animation.style}`)}}},_destroy:function(){this.element.empty()},getValue:function(t){const e="number"==typeof t?t:this.options.data.findIndex((e=>e.id===t));return-1!==e?this.options.data[e].value:null},getOption:function(t){return this.options[t]},setOption:function(t,e){this.options[t]=e,this._render()}})}(jQuery);