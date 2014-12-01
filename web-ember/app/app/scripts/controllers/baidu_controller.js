App.BaiduController = Ember.Controller.extend({
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
              type:'baidu',
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
                  var publishtime = (data.addtime).replace("T"," ")
                  var url = data.url
                   var newRow = "<tr><td><a href='"+url+"' target='_blank'>"+title+"</a></td><td>"+sitename+"</td><td>"+publishtime+"</td></tr>";
                  var strNewRow = "<tr><td><div class='media'><div class='media-body'> <h4 class='media-heading'><a href='" + url + "'>" + title + "</a></h4><p>" + content + "</p><p class='txt-green'>" + publishtime + " - " + sitename  + "</p></div> </div></td></tr>";
             
                  $("#dataTable1 tbody").append(strNewRow);
                });
              }
            }, function(err){
              console.trace(err.message);
            });
           
        }

    	}
  
}
 
});