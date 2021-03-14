<template>
  <div>
    <div id='timeseletor'>
      选择时间间隔：
      <el-radio v-model="timegap" label="6h" border size="mini">6h</el-radio>
      <el-radio v-model="timegap" label="12h" border size="mini">12h</el-radio>
      <el-radio v-model="timegap" label="1d" border size="mini">1d</el-radio>
      <el-radio v-model="timegap" label="3d" border size="mini">3d</el-radio>
      <el-radio v-model="timegap" label="7d" border size="mini">7d</el-radio>
    </div>
    <v-chart class="chart" :option="option" id="datachart" v-if="this.current_file != 'None'"/>
  </div>
</template>

<script>
import { use } from "echarts/core";
import { EventBus } from "../event-bus.js";
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
} from "echarts/components";
import { LineChart } from "echarts/charts";
import { CanvasRenderer } from "echarts/renderers";
import 'echarts/lib/component/dataZoom'
import { default as VChart, THEME_KEY } from "vue-echarts";
import axios from 'axios';

use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
]);

export default {
  name: "HelloWorld",
  components: {
    VChart,
  },
  provide: {
    [THEME_KEY]: "light",
  },
  data() {
    return {
      timegap:'6h',
      current_file: 'None',
      option: {
        title: {
          text: "折线图堆叠",
        },
        tooltip: {
          trigger: "axis",
        },
        legend: {
          // data: ["邮件营销", "联盟广告", "视频广告", "直接访问"],
          type: 'scroll',
          orient: 'vertical',
          left: '92%',
          data:[]
        },
        grid: {
          type: 'inside',
          left: "3%",
          right: "10%",
          bottom: "3%",
          containLabel: true,
        },
        toolbox: {
          feature: {
            saveAsImage: {},
          },
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: [],
        },
        yAxis: {
          type: "value",
        },
        dataZoom:[
          {
            type:'slider',
            start:10,
            end:20
          },
          {
            type:'inside',
            start:10,
            end:60
          }
        ],
        series: [
          // {
          //   name: "邮件营销",
          //   type: "line",
          //   stack: "总量",
          //   data: [120, 132, 101, 134, 90, 230, 210],
          // },
          // {
          //   name: "联盟广告",
          //   type: "line",
          //   stack: "总量",
          //   data: [220, 182, 191, 234, 290, 330, 310],
          // },
          // {
          //   name: "视频广告",
          //   type: "line",
          //   stack: "总量",
          //   data: [150, 232, 201, 154, 190, 330, 410],
          // },
          // {
          //   name: "直接访问",
          //   type: "line",
          //   stack: "总量",
          //   data: [320, 332, 301, 334, 390, 330, 320],
          // },
          // {
          //   name: "搜索引擎",
          //   type: "line",
          //   stack: "总量",
          //   data: [820, 932, 901, 934, 1290, 1330, 1320],
          // },
        ],
      },
    };
  },
  methods: {
    getData(file_name){
      axios.get('http://127.0.0.1:5000/get/'+file_name).then(response => {
        // this.writeObj(response.data[file_name])
        this.writeObj(response.data)
        var temp_x_date = []
        for(var j = 0;j<response.data['datas'].length;j++){
          var temp_name = 'kpi'+ j
          var temp_dict = {}
          temp_dict['name'] = temp_name
          temp_dict['type'] = 'line'
          temp_dict['stack'] = temp_name
          var temp_data = []
          
          for(var i = 0;i<response.data['datas'][j].length;i++){
            temp_data.push(response.data['datas'][j][i]);
            // console.log(i);
          }
          
          temp_dict['data'] = temp_data
          this.option.legend.data.push(temp_name)
          this.option.series.push(temp_dict)
        }
        for(var l=0;l<response.data['timestamp'].length;l++){
          temp_x_date.push(response.data['timestamp'][l])
        }
        if(temp_x_date[0]<10){
          alert('index!')
        }
        this.option.xAxis.data = temp_x_date;
      })
    },
    writeObj(obj){ 
      var description = ""; 
      for(var i in obj){ 
      var property=obj[i]; 
      description+=i+" = "+property+"\n"; 
      }
      console.log(description); 
    } 
  },
  mounted(){
    EventBus.$on('changeRow',msg => {
      this.option.data = []
      this.option.series = []
      this.getData(msg)
      this.current_file = msg
      console.log('current file:'+this.current_file)
    }),
    EventBus.$on('deleteRow', msg => {
      this.option.data = []
      this.option.series = []
      this.current_file = 'None'
    })
  }
};
</script>

<style scoped>
.chart {
  height: 500px;
}
</style>