webpackJsonp([20],{aRw8:function(t,a,e){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var s=e("mvHQ"),n=e.n(s),i=e("CaOM"),o=e("6u2u"),r=e("mtWM"),c=e.n(r),l=e("P9l9"),u=(e("Au9i"),e("POuD")),_={data:function(){return{nav_list:[{name:"全部",params:"",active:!0},{name:"待付款",params:"",active:!1},{name:"待发货",params:"",active:!1},{name:"待收货",params:"",active:!1},{name:"已完成",params:"",active:!1}],page_info:{page_num:1,page_size:10},isScroll:!0,total_count:0,bottom_show:!1,order_list:null}},inject:["reload"],components:{navList:o.a,bottomLine:u.a},mounted:function(){i.a.changeTitle("订单列表"),this.getOrderList(),this.getOrderNum()},methods:{changeRoute:function(t,a){switch(t){case"/brandDetail":this.$router.push({path:t,query:{pbid:a.pbid}});break;case"/orderDetail":case"/logisticsInformation":this.$router.push({path:t,query:{omid:a.omid}});break;case"/selectBack":this.$router.push({path:t,query:{product:n()(a),allOrder:1}});break;default:this.$router.push(t)}},navClick:function(t){this.page_info.page_num=1,this.total_count=0,this.bottom_show=!1;var a=[].concat(this.nav_list);if(a[t].active)return!1;for(var e=0;e<a.length;e++)a[e].active=!1;a[t].active=!0,this.nav_list=[].concat(a),this.getOrderList(a[t].status)},getOrderList:function(t){var a=this;c.a.get(l.a.order_list,{params:{token:localStorage.getItem("token"),page_num:this.page_info.page_num,page_size:this.page_info.page_size,omstatus:t}}).then(function(t){if(200==t.data.status){if(a.isScroll=!0,!(t.data.data.length>0))return a.order_list=null,a.page_info.page_num=1,a.total_count=0,!1;a.page_info.page_num>1?a.order_list=a.order_list.concat(t.data.data):a.order_list=t.data.data,a.page_info.page_num=a.page_info.page_num+1,a.total_count=t.data.total_count}})},getOrderNum:function(){var t=this;c.a.get(l.a.order_count,{params:{token:localStorage.getItem("token")}}).then(function(a){if(200==a.data.status){for(var e=0;e<a.data.data.length;e++)a.data.data[e].active=!1;a.data.data[0].active=!0,t.nav_list=[].concat(a.data.data)}})},touchMove:function(t){var a=i.a.getScrollTop(),e=i.a.getScrollHeight(),s=i.a.getClientHeight();if(console.log(a+s>=e-10),a+s>=e-10&&this.isScroll)if(this.isScroll=!1,this.order_list.length==this.total_count)this.bottom_show=!0;else for(var n=0;n<this.nav_list.length;n++)this.nav_list[n].active&&this.getOrderList(this.nav_list[n].status)},cancelOrder:function(t){var a=this;c.a.post(l.a.cancle_order+"?token="+localStorage.getItem("token"),{omid:t.omid}).then(function(t){200==t.data.status&&a.reload()})}}},v={render:function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"m-orderList",on:{touchmove:function(a){return a.stopPropagation(),t.touchMove(a)}}},[e("div",{staticClass:"m-nav"},[e("nav-list",{attrs:{navlist:t.nav_list},on:{navClick:t.navClick}})],1),t._v(" "),e("div",{staticClass:"m-orderList-content"},[t._l(t.order_list,function(a,s){return[e("div",{staticClass:"m-one-part",on:{click:function(e){t.changeRoute("/orderDetail",a)}}},[e("div",{staticClass:"m-order-store-tile"},[e("div",{on:{click:function(e){e.stopPropagation(),t.changeRoute("/brandDetail",a)}}},[e("span",{staticClass:"m-icon-store"}),t._v(" "),e("span",{staticClass:"m-store-name"},[t._v(t._s(a.pbname))]),t._v(" "),e("span",{staticClass:"m-icon-more"})]),t._v(" "),e("span",{staticClass:"m-red"},[t._v(t._s(a.omstatus_zh))])]),t._v(" "),e("div",{staticClass:"m-order-product-ul"},[t._l(a.order_part,function(a,s){return[e("div",{staticClass:"m-product-info"},[e("img",{staticClass:"m-product-img",attrs:{src:"",alt:""}}),t._v(" "),e("div",[e("p",{staticClass:"m-flex-between"},[e("span",{staticClass:"m-product-name"},[t._v(t._s(a.prtitle))]),t._v(" "),e("span",{staticClass:"m-price"},[t._v("￥"+t._s(t._f("money")(a.skuprice)))])]),t._v(" "),e("p",{staticClass:"m-flex-between"},[e("span",{staticClass:"m-product-label"},[t._l(a.skuattritedetail,function(s,n){return[e("span",[t._v(t._s(s))]),t._v(" "),n<a.skuattritedetail.length-1?e("span",[t._v("；")]):t._e()]})],2),t._v(" "),e("span",[t._v("x"+t._s(a.opnum))])])])])]}),t._v(" "),e("ul",{staticClass:"m-order-btn-ul"},[10==a.omstatus?e("li",{on:{click:function(e){e.stopPropagation(),t.changeRoute("/selectBack",a)}}},[t._v("\n              退款\n            ")]):t._e(),t._v(" "),20==a.omstatus||35==a.omstatus?e("li",{on:{click:function(e){e.stopPropagation(),t.changeRoute("/logisticsInformation",a)}}},[t._v("\n              查看物流\n            ")]):t._e(),t._v(" "),-40==a.omstatus||30==a.omstatus?e("li",[t._v("\n              删除订单\n            ")]):t._e(),t._v(" "),0==a.omstatus?e("li",{on:{click:function(e){e.stopPropagation(),t.cancelOrder(a)}}},[t._v("\n              取消订单\n            ")]):t._e(),t._v(" "),35==a.omstatus?e("li",{staticClass:"active",on:{click:function(a){a.stopPropagation(),t.changeRoute("/addComment")}}},[t._v("\n              评价\n            ")]):t._e(),t._v(" "),10==a.omstatus||20==a.omstatus?e("li",{staticClass:"active"},[t._v("\n              确认收货\n            ")]):t._e(),t._v(" "),0==a.omstatus?e("li",{staticClass:"active"},[t._v("\n              立即付款\n            ")]):t._e()])],2)])]})],2),t._v(" "),t.bottom_show?e("bottom-line"):t._e()],1)},staticRenderFns:[]};var d=e("VU/8")(_,v,!1,function(t){e("qH4/")},"data-v-b0202f8e",null);a.default=d.exports},"qH4/":function(t,a){}});
//# sourceMappingURL=20.0a29249a010afb981e29.js.map