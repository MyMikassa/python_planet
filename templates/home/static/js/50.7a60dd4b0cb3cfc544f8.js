webpackJsonp([50],{cqYi:function(t,e){},g4jH:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var o,s=n("mtWM"),i=n.n(s),a=n("P9l9"),c=n("Au9i"),m={afterOpen:function(){o=document.scrollingElement.scrollTop||document.body.scrollTop,document.body.classList.add("scroll"),document.body.style.top=-o+"px"},beforeClose:function(){document.body.classList.remove("scroll"),document.scrollingElement.scrollTop=o,document.body.scrollTop=o}},l={name:"detail",data:function(){return{show_modal:!1,news_info:null,page_info:{page_num:1,page_size:10},isScroll:!0,total_count:0,bottom_show:!1,comment_list:null,comment_one:null,comment_content:"",comment_index:null,show_comment:!1,timeOutEvent:null}},components:{bottomLine:n("POuD").a},mounted:function(){this.getNewsDetail()},methods:{changeRoute:function(t,e,n){"shtype"==e?this.$router.push({path:t,query:{shtype:n}}):this.$router.push({path:t})},changeModal:function(t,e){this[t]=e,e?m.afterOpen():(m.beforeClose(),this.comment_one=null),"show_modal"==t&&this.getComment()},getNewsDetail:function(){var t=this;i.a.get(a.a.get_news_content,{params:{neid:this.$route.query.neid,token:localStorage.getItem("token")}}).then(function(e){200==e.data.status&&(t.news_info=e.data.data)})},isLickClick:function(t){var e=this;if(1==this.news_info.is_favorite||1==this.news_info.is_trample)return!1;i.a.post(a.a.favorite_news+"?token="+localStorage.getItem("token"),{neid:this.$route.query.neid,tftype:t}).then(function(n){200==n.data.status&&(t?(e.news_info.favoritnumber=e.news_info.favoritnumber+1,e.news_info.is_favorite=1):(e.news_info.tramplenumber=e.news_info.tramplenumber-1,e.news_info.is_trample=1))})},getComment:function(){var t=this;i.a.get(a.a.get_news_comment,{params:{neid:this.$route.query.neid,token:localStorage.getItem("token"),page_num:this.page_info.page_num,page_size:this.page_info.page_size}}).then(function(e){200==e.data.status&&(t.isScroll=!0,e.data.data.length>0?(t.page_info.page_num>1?t.comment_list=t.comment_list.concat(e.data.data):t.comment_list=e.data.data,t.page_info.page_num=t.page_info.page_num+1,t.total_count=e.data.total_count):(t.comment_list=null,t.page_info.page_num=1,t.total_count=0,t.show_comment=!0))})},commentClick:function(t,e){this.show_comment=!this.show_comment,this.comment_one=t,this.comment_index=e},sureComment:function(){var t=this;i.a.post(a.a.create_comment+"?token="+localStorage.getItem("token"),{neid:this.$route.query.neid,nctext:this.comment_content,ncid:this.comment_one&&this.comment_one.ncid}).then(function(e){200==e.data.status&&(Object(c.Toast)("评论成功"),t.page_info.page_num>1&&(t.page_info.page_num=t.page_info.page_num-1),t.getComment(),t.comment_content="",t.show_comment=!show_comment)})},commentLike:function(t){var e=this;i.a.post(a.a.favorite_comment+"?token="+localStorage.getItem("token"),{ncid:this.comment_list[t].ncid}).then(function(n){if(200==n.data.status){var o=[].concat(e.comment_list);o[t].is_favorite?o[t].favorite_count=o[t].favorite_count-1:o[t].favorite_count=o[t].favorite_count+1,o[t].is_favorite=!o[t].is_favorite,e.comment_list=[].concat(o)}})},touchMove:function(t){var e=this.$refs.comment.scrollTop,n=this.$refs.comment.scrollHeight;e+this.$refs.comment.offsetHeight>=n-10&&this.isScroll&&(this.isScroll=!1,this.comment_list.length==this.total_count?this.bottom_show=!0:this.getComment())},gtouchstart:function(t,e,n){var o=this;return this.timeOutEvent=setTimeout(function(){o.longPress(t,e,n)},500),!1},gtouchend:function(t){return clearTimeout(this.timeOutEvent),this.timeOutEvent,!1},gtouchmove:function(){clearTimeout(this.timeOutEvent),this.timeOutEvent=0},longPress:function(t,e,n){this.timeOutEvent=0;var o=this;c.MessageBox.confirm("你确定要删除这条评论吗?").then(function(s){s&&i.a.post(a.a.del_comment+"?token="+localStorage.getItem("token"),{ncid:t.ncid}).then(function(t){Object(c.Toast)({message:t.data.message,duration:1e3}),200==t.data.status&&(console.log(o.comment_list,e),o.comment_list[e].reply.splice(n,1))})})}}},_={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"m-circle-detail"},[n("div",{staticClass:"m-selected-search"},[n("span",{staticClass:"m-icon-back",on:{click:function(e){t.changeRoute("/circle")}}}),t._v(" "),n("div",{staticClass:"m-search-input-box",on:{click:function(e){t.changeRoute("/search","shtype","news")}}},[n("span",{staticClass:"m-icon-search"}),t._v(" "),n("span",[t._v("搜索圈子关键词")])])]),t._v(" "),t.news_info?n("div",{staticClass:"m-circle-content"},[n("h3",{staticClass:"m-circle-title"},[t._v(t._s(t.news_info.netitle))]),t._v(" "),t._l(t.news_info.image,function(e,o){return t.news_info.image?[n("img",{staticClass:"m-circle-img",attrs:{src:e.niimage,alt:""}})]:t._e()}),t._v(" "),n("div",{staticClass:"m-content"},[n("p",[t._v(t._s(t.news_info.netext))]),t._v(" "),t.news_info.video?n("div",{staticClass:"m-video-box"},[n("video",{staticClass:"m-video",attrs:{src:t.news_info.video.nvvideo}}),t._v(" "),n("img",{staticClass:"m-video-img",attrs:{src:t.news_info.video.nvthumbnail,alt:""}}),t._v(" "),n("span",{staticClass:"m-video-time"},[t._v(t._s(t.news_info.video.nvduration))]),t._v(" "),n("span",{staticClass:"m-icon-video"})]):t._e()])],2):t._e(),t._v(" "),t.news_info?n("div",{staticClass:"m-circle-foot"},[n("div",{staticClass:"float-left"},[n("span",{staticClass:"m-icon-btn active",on:{click:function(e){e.stopPropagation(),t.isLickClick(1)}}},[n("span",{staticClass:"m-icon-zan"}),t._v(" "),n("span",[t._v("赞同"+t._s(t.news_info.favoritnumber))])]),t._v(" "),n("span",{staticClass:"m-icon-btn",on:{click:function(e){e.stopPropagation(),t.isLickClick(0)}}},[n("span",{staticClass:"m-icon-cai"}),t._v(" "),n("span",[t._v("踩"+t._s(t.news_info.tramplenumber))])])]),t._v(" "),n("span",{staticClass:"m-circle-comment float-right",on:{click:function(e){t.changeModal("show_modal",!0)}}},[t._v("评论")])]):t._e(),t._v(" "),t.show_modal?n("div",{staticClass:"m-comment-modal"},[n("div",{staticClass:"m-modal-state"},[n("span",{staticClass:"m-icon-close",on:{click:function(e){t.changeModal("show_modal",!1)}}}),t._v(" "),n("div",{staticClass:"m-modal-content"},[n("h3",[t._v("全部"+t._s(t.total_count)+"条评论")]),t._v(" "),n("div",{ref:"comment",staticClass:"m-scroll",on:{touchmove:function(e){return e.stopPropagation(),t.touchMove(e)}}},[n("ul",{staticClass:"m-comment-ul"},t._l(t.comment_list,function(e,o){return n("li",[n("img",{staticClass:"m-user-img",attrs:{src:e.user.usheader,alt:""}}),t._v(" "),n("div",{staticClass:"m-comment-text"},[n("div",[n("p",{staticClass:"m-user-name"},[t._v(t._s(e.user.usname))]),t._v(" "),n("p",[t._v(t._s(e.nctext))]),t._v(" "),n("div",{staticClass:"m-icon-list"},[n("span",[t._v(t._s(e.createtime))]),t._v(" "),n("div",[n("span",{staticClass:"m-icon-like",class:e.is_favorite?"active":"",on:{click:function(e){e.stopPropagation(),t.commentLike(o)}}}),t._v(" "),n("span",[t._v(t._s(e.favorite_count))]),t._v(" "),n("span",{staticClass:"m-icon-comment",on:{click:function(n){n.stopPropagation(),t.commentClick(e,o)}}}),t._v(" "),n("span",{on:{click:function(n){n.stopPropagation(),t.commentClick(e,o)}}},[t._v(t._s(e.reply_count))])])])]),t._v(" "),t._l(e.reply,function(e,s){return n("p",{staticClass:"m-comment-content",on:{click:function(n){n.stopPropagation(),t.commentClick(e,o)},touchstart:function(n){t.gtouchstart(e,o,s)},touchmove:function(e){t.gtouchmove()},touchend:function(n){t.gtouchend(e,o,s)}}},[n("span",{staticClass:"m-user-name"},[t._v(t._s(e.commentuser))]),t._v(" "),e.replieduser?n("span",{staticClass:"m-comment-back"},[t._v("回复")]):t._e(),t._v(" "),e.replieduser?n("span",{staticClass:"m-user-name m-mr"},[t._v(" "+t._s(e.replieduser))]):t._e(),t._v(" "),n("span",[t._v(t._s(e.nctext))])])})],2)])})),t._v(" "),t.bottom_show?n("bottom-line"):t._e()],1),t._v(" "),t.show_comment?n("p",{staticClass:"m-comment-input"},[n("input",{directives:[{name:"model",rawName:"v-model",value:t.comment_content,expression:"comment_content"}],attrs:{type:"text",placeholder:"请输入评论"},domProps:{value:t.comment_content},on:{input:function(e){e.target.composing||(t.comment_content=e.target.value)}}}),t._v(" "),n("span",{staticClass:"m-input-sure",on:{click:function(e){return e.stopPropagation(),t.sureComment(e)}}},[t._v("确定")])]):t._e()])])]):t._e()])},staticRenderFns:[]};var r=n("VU/8")(l,_,!1,function(t){n("cqYi")},"data-v-259919a2",null);e.default=r.exports}});
//# sourceMappingURL=50.7a60dd4b0cb3cfc544f8.js.map