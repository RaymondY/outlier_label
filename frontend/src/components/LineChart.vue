<template>
<div id = 'allchart' :style="{width: '100%', height: '80%'}">
  <div id='timeseletor'>
      选择时间间隔：
      <el-radio-group v-model="timegap">
        <el-radio :label=360 border size="mini">6h</el-radio>
        <el-radio :label=720 border size="mini">12h</el-radio>
        <el-radio :label=1440 border size="mini">1d</el-radio>
        <el-radio :label=4320 border size="mini">3d</el-radio>
        <el-radio :label=10080 border size="mini">7d</el-radio>
        <el-button size="mini" @click="changezoomer">确定</el-button>
      </el-radio-group>
  </div>
  <div id="myChart" ref="chart" :style="{width: '100%', height: '100%'} "></div>
</div>
</template>
<script>
import axios from 'axios';
// 引入基本模板
let echarts = require('echarts/lib/echarts')
import { EventBus } from "../event-bus.js";
// 引入柱状图组件
require('echarts/lib/chart/bar')
// 引入提示框和title组件
require('echarts/lib/component/tooltip')
require('echarts/lib/component/title')
export default {
  name: 'HelloWorld',
  data() {
    return {
      timegap:144,
      current_file: 'None',
      mingap:5,
      mychart : 'null'
    }
  },
  mounted() {
    this.drawLine();
    // document.getElementById('allchart').style.display = 'none';
    EventBus.$on('changeRow',msg => {
      document.getElementById('allchart').style.display = '';
      this.getData(msg)
      this.current_file = msg
      console.log('!!current file:'+this.current_file)
    })
    EventBus.$on('deleteRow', msg => {
      // this.option.data = []
      // this.option.series = []
      this.mychart.setOption({
        legend:{
            data:[]
          },
          series: [],
          xAxis:{
            data: [],
          }
      })
    })
  },
  methods: {
    drawLine() {
      // 基于准备好的dom，初始化echarts实例
      let myChart = echarts.init(document.getElementById('myChart'))
      this.mychart = myChart
      // 绘制图表
      myChart.setOption({
        title: { text: 'ECharts 入门示例' },
        tooltip: {},
        xAxis: {
          data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
        },
        yAxis: {},
        series: [],
        toolbox:{
          feature:{
            brush:{
              type:['rect']
            },
          }
        },
        brush:{
          xAxisIndex:'all',
          yAxisIndex:'all'
        },
        dataZoom:[
          {
            type:'slider',
            start:10,
            end:20
          },
        ],
      });
      myChart.on('brushSelected', renderBrushed);
        function renderBrushed(params) {
          var mainseries = params.batch[0].selected[0].dataIndex;
          console.log(mainseries)
        }
      document.getElementById('allchart').style.display = 'none';
    },
    getData(file_name){
      axios.get('http://127.0.0.1:5000/get/'+file_name).then(response => {
        // this.writeObj(response.data[file_name])
        this.writeObj(response.data)
        this.mingap = response.data.mingap
        var temp_x_date = [],namelist = [],serieslist =[]
        for(var j = 0;j<response.data['datas'].length;j++){
          var temp_name = 'kpi'+ j
          var temp_dict = {}
          temp_dict['name'] = temp_name
          temp_dict['type'] = 'line'
          var temp_data = []
          for(var i = 0;i<response.data['datas'][j].length;i++){
            temp_data.push(response.data['datas'][j][i]);
            // console.log(i);
          }
          
          temp_dict['data'] = temp_data
          namelist.push(temp_name)
          serieslist.push(temp_dict)
        }
        for(var l=0;l<response.data['timestamp'].length;l++){
          temp_x_date.push(response.data['timestamp'][l])
        }
        this.mychart.setOption({
          legend:{
            data:namelist
          },
          series: serieslist,
          xAxis:{
            data: temp_x_date,
          }
        })
      })
    },
    writeObj(obj){ 
      var description = ""; 
      for(var i in obj){ 
      var property=obj[i]; 
      description+=i+" = "+property+"\n"; 
      }
    },
    changezoomer(){
      console.log(this.mychart.getOption().dataZoom[0].startValue)
      var zoomerlen = parseInt(this.timegap/this.mingap)
      var tempoption = {
        dataZoom:[
          {
            type:'slider',
            startValue:this.mychart.getOption().dataZoom[0].startValue,
            endValue:this.mychart.getOption().dataZoom[0].startValue + zoomerlen
          }
        ]
      }
      this.mychart.setOption(tempoption)
      // this.$refs["echart"].getOp()
    } 
  }
}
</script>
