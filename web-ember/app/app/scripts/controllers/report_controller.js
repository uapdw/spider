App.ReportController = Ember.Controller.extend({
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
              type:'report',
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
                
                $("#data").empty();
                $.each(json.hits.hits,function(i,v){
                  data = v._source
                  dataHighLight = v.highlight
                  var title = dataHighLight.title
                  var sitename = data.sitename
                  var publishtime = (data.publishtime).replace("T"," ")
                  var url = data.url
                  var newRow = "<tr><td><a href='"+url+"' target='_blank'>"+title+"</a></td><td>"+sitename+"</td><td>"+publishtime+"</td></tr>"
             
                  $("#data").append(newRow);
                });
              }
            }, function(err){
              console.trace(err.message);
            });
        }

    	}
  
  
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