App.NewsController = Ember.Controller.extend({
	titleBinding: 'App.News.title',
	isSearched: false,
	actions: {
    	search: function () {
          isSearched: true;
          console.log("搜索");
      		var tit = this.get('newTitle');
      		if (!tit.trim()) { 
            alert("请输入关键词！");
      			//return; 
      		}else{
            keyword = $("#txtKeyword").val();

            client.search({
              index:'web-articles',
              type:'article',
              size:50,
              body:{
                query:{
                  match:{
                    title:keyword
                  }
                },
                sort:{
                  publishtime:{
                    order:"desc"
                  }
                },
                highlight:{
                  tags_schema:'styled',
                  fields:{
                    title:{}
                  }
                }
              }
            }).then(function(json){
              if(json.hits.total == 0){
                alert('没有您要搜索的数据！');
              }else{
                
                $("#dataTable1 tbody").empty();
                $.each(json.hits.hits,function(i,v){
                  data = v._source
                  dataHighLight = v.highlight
                  if(v.highlight && dataHighLight.title){
                    var title = dataHighLight.title
                  }else{
                    var title = data.title
                  }
                  var sitename = data.sitename
                  if(v.highlight && dataHighLight.content){
                    var content = dataHighLight.content + '...'
                  }else{
                    var content = subString((data.content).replace(/<\/?[^>]*>/g,''),200,true);
                        }
                  var publishtime = (data.publishtime).replace("T"," ")
                  var url = data.url
                  var newRow = "<tr><td><a href='"+url+"' target='_blank'>"+title+"</a></td><td>"+sitename+"</td><td>"+publishtime+"</td></tr>";
                  var strNewRow = "<tr><td><div class='media'><div class='media-body'> <h4 class='media-heading'><a href='" + url + "'>" + title + "</a></h4><p>" + content + "</p><p class='txt-green'>" + publishtime + " - " + sitename  + "</p></div> </div></td></tr>";
             
                  $("#dataTable1 tbody").append(strNewRow);
                });
              }
            }, function(err){
              console.trace(err.message);
            });
            //alert("This is the result！");
         // window.location.reload();

      		//this.set('title', tit);
      		//this.set('newTitle', '');
        }

    	}
   //   
  
}
 


    // $.getJSON('172.20.8.3:9200',{
    //   format:"json"
    // },
    // function(data){
    //     alert("aaa");
    // })
    // isCurrentItem: function(){
    //     this.get
    // }
//    clickTosearch: function(){
//        this.toggleProperty('isShowingBody');
//    },
  	
  //   isClicked: function(key, value){
  // 		// var model = this.get('model');
  // 		this.set('isClicked', value);

 	// 	// if(value) {
 	// 	// 	this.set('hello', 'click');
 	// 	// } else {
 	// 	// 	this.set('hello', 'no click');
 	// 	// }

 	// 	// var date = new Date();
 	// 	// this.set('date', new Date());

 	// 	return this.get('isClicked');
 	// }.property('model.isClicked')


});