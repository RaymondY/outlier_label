<template>
  <v-chart class="chart" :option="option" />
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
        console.log(response.data[file_name][0].length)
        console.log(response.data[file_name].length)
        for(var j = 0;j<response.data[file_name].length;j++){
          var temp_name = 'kpi'+ j
          var temp_dict = {}
          temp_dict['name'] = temp_name
          temp_dict['type'] = 'line'
          temp_dict['stack'] = temp_name
          var temp_data = []
          var temp_x_date = []
          for(var i = 0;i<response.data[file_name][j].length;i++){
            temp_data.push(response.data[file_name][j][i]);
            temp_x_date.push(i);
            // console.log(i);
          }
          this.option.xAxis.data = temp_x_date;
          temp_dict['data'] = temp_data
          this.option.legend.data.push(temp_name)
          this.option.series.push(temp_dict)
        }
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
      console.log(msg)
    })
  }
};
</script>

<style scoped>
.chart {
  height: 500px;
}
</style>