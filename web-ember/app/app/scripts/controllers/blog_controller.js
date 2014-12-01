App.BlogController = Ember.Controller.extend({
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
              type:'blog',
              size:50,
              body:{
                query:{
                  match:{
                    title:keyword
                  }
                },
                sort:{
                  addtime:{
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
                
                $("#dataTable tbody").empty();
                $.each(json.hits.hits,function(i,v){
                  data = v._source
                  dataHighLight = v.highlight
                  var title = dataHighLight.title
                  var sitename = data.sitename
                  var publishtime = (data.addtime).replace("T"," ")
                  var url = data.url
                  var newRow = "<tr><td><a href='"+url+"' target='_blank'>"+title+"</a></td><td>"+sitename+"</td><td>"+publishtime+"</td></tr>"
             
                  $("#dataTable tbody").append(newRow);
                });
              }
            }, function(err){
              console.trace(err.message);
            });
           
        }

    	}
  
}
 
});