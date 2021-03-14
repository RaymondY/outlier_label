<template>
  <div id = "mainchart" v-if="this.current_file != 'None'">
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
    <div>
      <v-chart class="chart" :option="option" id="datachart" ref="echart"/>
    </div>
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
      timegap:144,
      current_file: 'None',
      mingap:5,
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
        ],
        series: [
        ],
      },
    };
  },
  methods: {
    getData(file_name){
      axios.get('http://127.0.0.1:5000/get/'+file_name).then(response => {
        // this.writeObj(response.data[file_name])
        this.writeObj(response.data)
        this.mingap = response.data.mingap
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
        this.option.xAxis.data = temp_x_date;
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
      console.log(this.$refs["echart"].getOption().dataZoom[0].startValue)
      var zoomerlen = parseInt(this.timegap/this.mingap)
      var tempoption = {
        dataZoom:[
          {
            type:'slider',
            startValue:this.$refs["echart"].getOption().dataZoom[0].startValue,
            endValue:this.$refs["echart"].getOption().dataZoom[0].startValue + zoomerlen
          }
        ]
      }
      this.$refs["echart"].setOption(tempoption)
      // this.$refs["echart"].getOp()
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
#mainchart {
  margin-top: 5px;
}
</style>