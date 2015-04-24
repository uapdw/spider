// vim: set et sw=2 ts=2 sts=2 ff=unix fenc=utf8:
// Author: Binux<i@binux.me>
//         http://binux.me
// Created on 2014-03-02 17:53:23

$(function() {
  /*$(".project-group>span").editable({
    name: 'group',
    pk: function(e) {
      return $(this).parents('tr').data("name");
    },
    emptytext: '[group]',
    placement: 'right',
    url: "/update"
  });*/

  /*$(".project-status>span").editable({
    type: 'select',
    name: 'status',
    source: [
      {value: 'TODO', text: 'TODO'},
      {value: 'STOP', text: 'STOP'},
      {value: 'CHECKING', text: 'CHECKING'},
      {value: 'DEBUG', text: 'DEBUG'},
      {value: 'RUNNING', text: 'RUNNING'}
    ],
    pk: function(e) {
      return $(this).parents('tr').data("name");
    },
    emptytext: '[status]',
    placement: 'right',
    url: "/update",
    success: function(response, value) {
      $(this).removeClass('status-'+$(this).attr('data-value')).addClass('status-'+value).attr('data-value', value).attr('style', '');
    }
  });*/

  $(".project-rate>span").editable({
    name: 'rate',
    pk: function(e) {
      return $(this).parents('tr').data("name");
    },
    validate: function(value) {
      var s = value.split('/');
      if (s.length != 2)
        return "format error: rate/burst";
      if (!$.isNumeric(s[0]) || !$.isNumeric(s[1]))
        return "format error: rate/burst";
    },
    highlight: false,
    emptytext: '0/0',
    placement: 'right',
    url: "/update"
  });

  $('.project-create').on('click', function() {
    //var result = prompt('请输入爬虫名称（只允许使用英文字母、数字和下划线）:');
    var spiderName = $('#cs_spiderName').val();
    var groupName = $('#cs_groupName').val();
    //alert(spiderName + ' ### ' + groupName);

    if (spiderName && spiderName.search(/[^\w]/) == -1) {
      location.href = "/edit/"+groupName+"/"+spiderName;
    } else {
      alert('爬虫名称格式不正确！');
    }
  });

  $('.project-run').on('click', function() {
    var spiderName = $(this).parents('tr').data("name");
    var groupName = $(this).parents('tr').data('group');
    //alert(spiderName + ' ### ' + groupName);
    var _this = this;
    //$(this).addClass("btn-warning");
    $.ajax({
      type: "POST",
      url: '/run',
      data: {
        spiderName: spiderName,
        groupName: groupName
      },
      success: function(data) {
        console.log(data);
        var jsonObj = eval('(' + data + ')');
        $(_this).removeClass("btn-warning");
        if (jsonObj.status != 'ok') {
          $(_this).addClass("btn-danger");
          alert(groupName+'分组的爬虫'+spiderName+'运行失败，请查看scrapyd服务的状态！');
        }else{
          $(_this).addClass("btn-success");
          alert(groupName+'分组的爬虫'+spiderName+'已开始运行，请到任务列表中查看运行状态！');
        }
      },
      error: function() {
        $(_this).removeClass("btn-warning").addClass("btn-danger");
      }
    });
  });


  $('.project-cancel').on('click', function() {
    var jobId = $(this).parents('tr').data("id");
    var groupName = $(this).parents('tr').data('group');
    //alert(jobId + ' ### ' + groupName);
    var _this = this;
    //$(this).addClass("btn-warning");
    $.ajax({
      type: "POST",
      url: '/cancel',
      data: {
        jobId: jobId,
        groupName: groupName
      },
      success: function(data) {
        console.log(data);
        var jsonObj = eval('(' + data + ')');
        $(_this).removeClass("btn-warning");
        if (jsonObj.status != 'ok') {
          $(_this).addClass("btn-danger");
          alert(groupName+'分组中ID为'+jobId+'的爬虫取消失败，请查看scrapyd服务的状态！');
        }else{
          $(_this).addClass("btn-success");
          alert(groupName+'分组中ID为'+jobId+'的爬虫已取消！');
        }
      },
      error: function() {
        $(_this).removeClass("btn-warning").addClass("btn-danger");
      }
    });
  });

  $('#btnGotoJobList').on('click', function(){
    groupName = $('#job_groupName').val()
    location.href = '/joblist/'+groupName

  });

  $('#btnDeploySpider').on('click', function(){
    groupName = $('#deploy_groupName').val()
    //alert(groupName);
    //location.href = '/joblist/'+groupName
    $.ajax({
      type: "POST",
      url: '/deploy',
      data: {
        groupName: groupName
      },
      success: function(data) {
        console.log(data);
        var jsonObj = eval('(' + data + ')');
        //alert(jsonObj.status);
        if(jsonObj.status == 'ok'){
          alert('成功部署分组：'+groupName + '！');
        }else{
          alert("部署分组："+groupName+"失败，scrapyd服务出现问题！");
        }

        $('#deploySpiderModal').modal('toggle');
        //alert("deploy finished!");
      },
      error: function() {
        console.log('部署分组："+groupName+"失败，未能成功提交数据！');
      }
    });

  });

  $('#btnShowResult').on('click', function(){
    resultsType = $('#resultsType').val()
    location.href = '/resultslist/'+resultsType

  });

  $('.btn-returnSpiderList').on('click', function(){
    location.href='/spiderlist'
  });

  // onload
  function fill_progress(data, type) {
    console.log(data);
    $.each(data, function(project, info) {
      var $e = $("tr[data-name="+project+"] td.progress-"+type);
      var pending = info.pending || 0,
          success = info.success || 0,
          retry = info.retry || 0,
          failed = info.failed || 0,
          sum = info.task || pending + success + retry + failed;
      $e.attr("title", ""+type+" of "+sum+" tasks:\n"
              +(type == "all"
                ? "pending("+(pending/sum*100).toFixed(1)+"%): \t"+pending+"\n"
                : "new("+(pending/sum*100).toFixed(1)+"%): \t\t"+pending+"\n")
              +"success("+(success/sum*100).toFixed(1)+"%): \t"+success+"\n"
              +"retry("+(retry/sum*100).toFixed(1)+"%): \t"+retry+"\n"
              +"failed("+(failed/sum*100).toFixed(1)+"%): \t"+failed
             );
      $e.attr('data-value', sum);
      $e.find(".progress-text").text(type+": "+sum);
      $e.find(".progress-pending").width(""+(pending/sum*100)+"%");
      $e.find(".progress-success").width(""+(success/sum*100)+"%");
      $e.find(".progress-retry").width(""+(retry/sum*100)+"%");
      $e.find(".progress-failed").width(""+(failed/sum*100)+"%");
    });
  }
 /* function update_counters() {
    $.get('/counter?time=5m&type=sum', function(data) {
      fill_progress(data, "5m");
    });
    $.get('/counter?time=1h&type=sum', function(data) {
      fill_progress(data, "1h");
    });
    $.get('/counter?time=1d&type=sum', function(data) {
      fill_progress(data, "1d");
    });
    $.get('/counter?time=all&type=sum', function(data) {
      fill_progress(data, "all");
    });
  }
  window.setInterval(update_counters, 15*1000);
  update_counters();*/

  // table sortable
  Sortable.getColumnType = function(table, i) {
    var type = $($(table).find('th').get(i)).data('type');
    if (type == "num") {
      return Sortable.types.numeric;
    } else if (type == "date") {
      return Sortable.types.date;
    }
    return Sortable.types.alpha;
  };
  $('table.projects').attr('data-sortable', true);
  Sortable.init();
});
