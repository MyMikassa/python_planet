webpackJsonp([61],{MGkp:function(e,t,i){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=i("CaOM"),a=i("mtWM"),s=i.n(a),c=i("P9l9"),m={data:function(){return{name:"",icon_list:[{name:"登山徒步",src:"/static/images/equipment/equipment-mountaineering.png",url:""},{name:"露营装备",src:"/static/images/equipment/equipment-camping.png",url:""},{name:"运动健身",src:"/static/images/equipment/equipment-fitness.png",url:""},{name:"旅行用品",src:"/static/images/equipment/equipment-travel.png",url:""},{name:"数码电子",src:"/static/images/equipment/equipment-electronic.png",url:""},{name:"水上运动",src:"/static/images/equipment/equipment-water.png",url:""},{name:"游泳运动",src:"/static/images/equipment/equipment-swim.png",url:""},{name:"儿童户外",src:"/static/images/equipment/equipment-child.png",url:""},{name:"骑行运动",src:"/static/images/equipment/equipment-riding.png",url:""},{name:"户外食品",src:"/static/images/equipment/equipment-outdoor.png",url:""},{name:"滑雪运动",src:"/static/images/equipment/equipment-ski.png",url:""},{name:"潜水运动",src:"/static/images/equipment/equipment-dive.png",url:""}]}},components:{},mounted:function(){n.a.changeTitle("装备"),this.getCategory()},methods:{changeRoute:function(e,t){t?this.$router.push({path:e}):this.$router.push({path:"/equipment/detail",query:{head:e.pcpic,name:e.pcname,pcid:e.pcid}})},getCategory:function(){var e=this;s.a.get(c.a.category_list).then(function(t){200==t.data.status&&(e.icon_list=[].concat(t.data.data))})}},created:function(){}},u={render:function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"m-equipment"},[i("div",{staticClass:"m-selected-search"},[i("div",{staticClass:"m-search-input-box",on:{click:function(t){e.changeRoute("/search","top")}}},[i("span",{staticClass:"m-icon-search"}),e._v(" "),i("span",[e._v("搜索商品")])])]),e._v(" "),e._m(0),e._v(" "),i("div",{staticClass:"m-equipment-icon-box"},[i("ul",{staticClass:"m-equipment-icon-ul"},e._l(e.icon_list,function(t,n){return i("li",{on:{click:function(i){e.changeRoute(t)}}},[i("img",{attrs:{src:t.pcpic,alt:""}}),e._v(" "),i("span",{staticClass:"m-name"},[e._v(e._s(t.pcname))])])}))])])},staticRenderFns:[function(){var e=this.$createElement,t=this._self._c||e;return t("div",{staticClass:"m-equipment-img-box"},[t("img",{staticClass:"m-equipment-img",attrs:{src:"",alt:""}}),this._v(" "),t("span",{staticClass:"mm-equipment-bg"})])}]};var r=i("VU/8")(m,u,!1,function(e){i("bQXx")},"data-v-038ea31c",null);t.default=r.exports},bQXx:function(e,t){}});
//# sourceMappingURL=61.2e47b06ac925a154a724.js.map