webpackJsonp([57],{OSUD:function(t,i){},dR6F:function(t,i,s){"use strict";Object.defineProperty(i,"__esModule",{value:!0});var m=s("CaOM"),a={name:"orderManagement",data:function(){return{navList:[{name:"所有订单(17)",active:!0},{name:"待发货(1)",active:!1},{name:"已发货(1)",active:!1},{name:"退货(1)",active:!1}]}},components:{navList:s("6u2u").a},methods:{navClick:function(t){for(var i=[].concat(this.navList),s=0;s<i.length;s++)i[s].active=!1;i[t].active=!0,this.navList=[].concat(i)},changeRoute:function(t){this.$router.push(t)}},mounted:function(){m.a.changeTitle("订单管理")}},r={render:function(){var t=this,i=t.$createElement,s=t._self._c||i;return s("div",{staticClass:"m-order-management"},[s("div",{staticClass:"m-nav"},[s("navList",{attrs:{navlist:t.navList,isScroll:!1},on:{navClick:t.navClick}})],1),t._v(" "),s("div",{staticClass:"m-order-box"},[t._m(0),t._v(" "),t._m(1),t._v(" "),s("div",{staticClass:"m-order-item"},[t._m(2),t._v(" "),t._m(3),t._v(" "),t._m(4),t._v(" "),s("div",{staticClass:"m-order-time-btn"},[s("div",{staticClass:"m-order-time m-color-999"},[t._v("2018-08-08 16:49:07 创建")]),t._v(" "),s("div",{staticClass:"m-order-btn m-color-white m-btn-yellow",on:{click:function(i){t.changeRoute("/storekeeper/delivery")}}},[t._v("发 货")])])])])])},staticRenderFns:[function(){var t=this,i=t.$createElement,s=t._self._c||i;return s("div",{staticClass:"m-order-item"},[s("div",{staticClass:"m-item-row"},[s("div",{staticClass:"m-item-row-left m-color-666"},[t._v("订单号：123456789000")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-color-999"},[t._v("待发货")])]),t._v(" "),s("div",{staticClass:"m-product-box"},[s("div",{staticClass:"m-product-item"},[s("div",{staticClass:"m-product-left"},[s("img",{staticClass:"m-product-img",attrs:{src:"http://dummyimage.com/175x175",alt:""}})]),t._v(" "),s("div",{staticClass:"m-product-right"},[s("div",{staticClass:"m-product-name"},[t._v("商品名称")]),t._v(" "),s("div",{staticClass:"m-item-row m-color-999 m-margin"},[s("div",{staticClass:"m-item-row-left"},[t._v("规格：黑色-42码")]),t._v(" "),s("div",{staticClass:"m-item-row-right"},[t._v("数量：x1")])]),t._v(" "),s("div",{staticClass:"m-item-row m-color-666 m-width-80"},[s("div",{staticClass:"m-item-row-left m-ft-24"},[t._v("付款金额")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-24"},[t._v("成交预估收入")])]),t._v(" "),s("div",{staticClass:"m-item-row m-ft-b m-color-red m-width-70"},[s("div",{staticClass:"m-item-row-left m-ft-28"},[t._v("￥29.36")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-28"},[t._v("￥2.36")])])])])]),t._v(" "),s("div",{staticClass:"m-item-row m-color-999 m-margin"},[s("div",{staticClass:"m-item-row-left"},[t._v("共 5 件商品 合计："),s("span",{staticClass:"m-color-red"},[t._v("￥153.26")])]),t._v(" "),s("div",{staticClass:"m-item-row-right"},[t._v("总预估收入："),s("span",{staticClass:"m-color-red"},[t._v("￥22.36")])])]),t._v(" "),s("div",{staticClass:"m-order-time-btn"},[s("div",{staticClass:"m-order-time m-color-999"},[t._v("2018-08-08 16:49:07 创建")]),t._v(" "),s("div",{staticClass:"m-order-btn m-color-white m-btn-grey"},[t._v("退货中")])])])},function(){var t=this,i=t.$createElement,s=t._self._c||i;return s("div",{staticClass:"m-order-item"},[s("div",{staticClass:"m-item-row"},[s("div",{staticClass:"m-item-row-left m-color-666"},[t._v("订单号：123456789000")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-color-999"},[t._v("待发货")])]),t._v(" "),s("div",{staticClass:"m-product-box"},[s("div",{staticClass:"m-product-item"},[s("div",{staticClass:"m-product-left"},[s("img",{staticClass:"m-product-img",attrs:{src:"http://dummyimage.com/175x175",alt:""}})]),t._v(" "),s("div",{staticClass:"m-product-right"},[s("div",{staticClass:"m-product-name"},[t._v("商品名称")]),t._v(" "),s("div",{staticClass:"m-item-row m-color-999 m-margin"},[s("div",{staticClass:"m-item-row-left"},[t._v("规格：黑色-42码")]),t._v(" "),s("div",{staticClass:"m-item-row-right"},[t._v("数量：x1")])]),t._v(" "),s("div",{staticClass:"m-item-row m-color-666 m-width-80"},[s("div",{staticClass:"m-item-row-left m-ft-24"},[t._v("付款金额")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-24"},[t._v("成交预估收入")])]),t._v(" "),s("div",{staticClass:"m-item-row m-ft-b m-color-red m-width-70"},[s("div",{staticClass:"m-item-row-left m-ft-28"},[t._v("￥29.36")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-28"},[t._v("￥2.36")])])])])]),t._v(" "),s("div",{staticClass:"m-item-row m-color-999 m-margin"},[s("div",{staticClass:"m-item-row-left"},[t._v("共 5 件商品 合计："),s("span",{staticClass:"m-color-red"},[t._v("￥153.26")])]),t._v(" "),s("div",{staticClass:"m-item-row-right"},[t._v("总预估收入："),s("span",{staticClass:"m-color-red"},[t._v("￥22.36")])])]),t._v(" "),s("div",{staticClass:"m-order-time-btn"},[s("div",{staticClass:"m-order-time m-color-999"},[t._v("2018-08-08 16:49:07 创建")]),t._v(" "),s("div",{staticClass:"m-order-btn m-color-white m-btn-red"},[t._v("申请退款")])])])},function(){var t=this.$createElement,i=this._self._c||t;return i("div",{staticClass:"m-item-row"},[i("div",{staticClass:"m-item-row-left m-color-666"},[this._v("订单号：123456789000")]),this._v(" "),i("div",{staticClass:"m-item-row-right m-color-999"},[this._v("待发货")])])},function(){var t=this,i=t.$createElement,s=t._self._c||i;return s("div",{staticClass:"m-product-box"},[s("div",{staticClass:"m-product-item"},[s("div",{staticClass:"m-product-left"},[s("img",{staticClass:"m-product-img",attrs:{src:"http://dummyimage.com/175x175",alt:""}})]),t._v(" "),s("div",{staticClass:"m-product-right"},[s("div",{staticClass:"m-product-name"},[t._v("商品名称")]),t._v(" "),s("div",{staticClass:"m-item-row m-color-999 m-margin"},[s("div",{staticClass:"m-item-row-left"},[t._v("规格：黑色-42码")]),t._v(" "),s("div",{staticClass:"m-item-row-right"},[t._v("数量：x1")])]),t._v(" "),s("div",{staticClass:"m-item-row m-color-666 m-width-80"},[s("div",{staticClass:"m-item-row-left m-ft-24"},[t._v("付款金额")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-24"},[t._v("成交预估收入")])]),t._v(" "),s("div",{staticClass:"m-item-row m-ft-b m-color-red m-width-70"},[s("div",{staticClass:"m-item-row-left m-ft-28"},[t._v("￥29.36")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-28"},[t._v("￥2.36")])])])]),t._v(" "),s("div",{staticClass:"m-product-item"},[s("div",{staticClass:"m-product-left"},[s("img",{staticClass:"m-product-img",attrs:{src:"http://dummyimage.com/175x175",alt:""}})]),t._v(" "),s("div",{staticClass:"m-product-right"},[s("div",{staticClass:"m-product-name"},[t._v("商品名称")]),t._v(" "),s("div",{staticClass:"m-item-row m-color-999 m-margin"},[s("div",{staticClass:"m-item-row-left"},[t._v("规格：黑色-42码")]),t._v(" "),s("div",{staticClass:"m-item-row-right"},[t._v("数量：x1")])]),t._v(" "),s("div",{staticClass:"m-item-row m-color-666 m-width-80"},[s("div",{staticClass:"m-item-row-left m-ft-24"},[t._v("付款金额")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-24"},[t._v("成交预估收入")])]),t._v(" "),s("div",{staticClass:"m-item-row m-ft-b m-color-red m-width-70"},[s("div",{staticClass:"m-item-row-left m-ft-28"},[t._v("￥29.36")]),t._v(" "),s("div",{staticClass:"m-item-row-right m-ft-28"},[t._v("￥2.36")])])])])])},function(){var t=this.$createElement,i=this._self._c||t;return i("div",{staticClass:"m-item-row m-color-999 m-margin"},[i("div",{staticClass:"m-item-row-left"},[this._v("共 5 件商品 合计："),i("span",{staticClass:"m-color-red"},[this._v("￥153.26")])]),this._v(" "),i("div",{staticClass:"m-item-row-right"},[this._v("总预估收入："),i("span",{staticClass:"m-color-red"},[this._v("￥22.36")])])])}]};var v=s("VU/8")(a,r,!1,function(t){s("OSUD")},"data-v-09034880",null);i.default=v.exports}});
//# sourceMappingURL=57.c88148132d93d86cdcb0.js.map