webpackJsonp([37],{"04w7":function(t,a){},"4SR7":function(t,a,o){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var n=o("BpNX"),s=o("6u2u"),e=o("CaOM"),i=o("mtWM"),u=o.n(i),c=o("P9l9"),l=o("Au9i"),r=o("POuD"),p={data:function(){return{nav_list:[{name:"未使用",params:"2",active:!0},{name:"已使用",params:"1",active:!1},{name:"已过期",params:"0",active:!1}],couponList:[],status:"2",page_num:1,page_size:10,isScroll:!0,total_count:0,bottom_show:!1}},inject:["reload"],components:{navList:s.a,couponCard:n.a,bottomLine:r.a},methods:{navClick:function(t){this.page_num=1,this.total_count=0,this.bottom_show=!1;for(var a=[].concat(this.nav_list),o=0;o<a.length;o++)a[o].active=!1;a[t].active=!0,this.status=a[t].params,this.getUserCoupon(),this.nav_list=[].concat(a)},getUserCoupon:function(){var t=this,a={token:localStorage.getItem("token"),page_num:this.page_num,page_size:this.page_size};"0"==this.status?a.canuse="false":"1"==this.status?a.ucalreadyuse="true":"2"==this.status&&(a.ucalreadyuse="false"),u.a.get(c.a.list_user_coupon,{params:a}).then(function(a){if(200!=a.data.status)return Object(l.Toast)(a.data.message),t.couponList=[],t.page_num=1,t.total_count=0,!1;if(t.isScroll=!0,a.data.data.length>0){if(t.page_num>1){for(var o=[],n=0;n<a.data.data.length;n++)o.push(a.data.data[n].coupon);t.couponList=t.couponList.concat(o)}else for(var s=0;s<a.data.data.length;s++)t.couponList.push(a.data.data[s].coupon);t.page_num=t.page_num+1,t.total_count=a.data.total_count}})},touchMove:function(t){var a=e.a.getScrollTop(),o=e.a.getScrollHeight();a+e.a.getClientHeight()>=o-10&&this.isScroll&&(this.isScroll=!1,this.couponList.length==this.total_count?this.bottom_show=!0:this.getUserCoupon())},loadTop:function(){this.reload()}},mounted:function(){e.a.changeTitle("我的优惠券"),this.getUserCoupon()}},h={render:function(){var t=this,a=t.$createElement,o=t._self._c||a;return o("div",{staticClass:"m-coupon",on:{touchmove:function(a){return a.stopPropagation(),t.touchMove(a)}}},[o("mt-loadmore",{attrs:{"top-method":t.loadTop}},[o("div",{staticClass:"m-nav"},[o("nav-list",{attrs:{navlist:t.nav_list,isScroll:!1},on:{navClick:t.navClick}})],1),t._v(" "),o("div",{staticClass:"m-coupon-content"},[o("coupon-card",{attrs:{couponList:t.couponList}})],1),t._v(" "),t.bottom_show?o("bottom-line"):t._e()],1)],1)},staticRenderFns:[]};var m=o("VU/8")(p,h,!1,function(t){o("04w7")},"data-v-551471af",null);a.default=m.exports}});
//# sourceMappingURL=37.73ebbe0ed9fb9278f043.js.map