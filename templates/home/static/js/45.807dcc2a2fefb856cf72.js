webpackJsonp([45],{"2iDe":function(t,s,i){"use strict";Object.defineProperty(s,"__esModule",{value:!0});var a=i("CaOM"),o=i("mtWM"),n=i.n(o),e=i("P9l9"),r=(i("Au9i"),{data:function(){return{order_info:"",logistic_info:null}},components:{},mounted:function(){a.a.changeTitle("物流信息"),this.getOrderInfo()},methods:{getOrderInfo:function(){var t=this;n.a.get(e.a.order_get,{params:{token:localStorage.getItem("token"),omid:this.$route.query.omid}}).then(function(s){200==s.data.status&&(t.order_info=s.data.data,s.data.data.omstatus>=20&&t.getLogistic())})},getLogistic:function(){var t=this;n.a.get(e.a.get_logistic,{params:{omid:this.$route.query.omid}}).then(function(s){200==s.data.status&&(t.logistic_info=s.data.data.oldata)})}},created:function(){}}),_={render:function(){var t=this,s=t.$createElement,i=t._self._c||s;return t.order_info?i("div",{staticClass:"m-logisticsInformation"},[i("div",{staticClass:"m-one-part"},[t._l(t.order_info.order_part,function(s,a){return[i("p",[t._v("商品："+t._s(s.prtitle))]),t._v(" "),i("div",{staticClass:"m-logisticsInformation-product-info"},[i("img",{attrs:{src:s.prmainpic,alt:""}}),t._v(" "),i("div",[i("p",[t._v("订单号："+t._s(t.order_info.omno))]),t._v(" "),i("div",{staticClass:"m-product-sku-price"},[i("p",[i("span",[t._v("规格：")]),t._v(" "),i("span",[t._l(s.skuattritedetail,function(a,o){return[i("span",[t._v(t._s(a))]),t._v(" "),o<s.skuattritedetail.length-1?i("span",[t._v("；")]):t._e()]})],2)]),t._v(" "),i("p",[i("span",[t._v("付款金额:")]),t._v(" "),i("span",{staticClass:"m-price"},[t._v("￥"+t._s(t._f("money")(s.opsubtotal)))])])])])])]})],2),t._v(" "),i("div",{staticClass:"m-one-part"},[t.logistic_info?i("p",{staticClass:"m-flex-between"},[i("span",[t._v("物流："+t._s(t.logistic_info.expName))]),t._v(" "),i("span",{staticClass:"m-ft-20"},[t._v("物流单号："+t._s(t.logistic_info.olexpressno))])]):t._e(),t._v(" "),i("p",{staticClass:"m-flex-between m-mt-15"},[i("span",[t._v("收货人："+t._s(t.order_info.omrecvname))]),t._v(" "),i("span",[t._v("联系电话："+t._s(t.order_info.omrecvphone))])]),t._v(" "),i("p",[t._v("\n      收货地址："+t._s(t.order_info.omrecvaddress)+"\n    ")])]),t._v(" "),t.logistic_info?i("div",{staticClass:"m-logisticsInformation-text"},[i("p",[t._v("物流信息：")]),t._v(" "),i("ul",{staticClass:"m-logisticsInformation-ul"},t._l(t.logistic_info.list,function(s,a){return i("li",[i("div",{staticClass:"m-time"},[i("p",[t._v(t._s(s.time))])]),t._v(" "),i("div",{staticClass:"m-logisticsInformation-info"},[i("span",{staticClass:"m-circle ",class:0==a||a==t.logistic_info.list.length-1?"active":""}),t._v(" "),i("span",{class:0==a?"m-top":a==t.logistic_info.list.length-1?"m-bottom":""}),t._v(" "),i("p",{staticClass:"m-ft-22"},[t._v(t._s(s.status))])])])}))]):t._e()]):t._e()},staticRenderFns:[]};var c=i("VU/8")(r,_,!1,function(t){i("gwaQ")},"data-v-343bcb8d",null);s.default=c.exports},gwaQ:function(t,s){}});
//# sourceMappingURL=45.807dcc2a2fefb856cf72.js.map