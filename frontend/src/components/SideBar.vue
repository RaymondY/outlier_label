<template>
  <div>
    <el-upload
      class="upload-demo"
      ref="upload"
      action="string"
      :limit="10"
      :multiple="false"
      :show-file-list="false"
      :http-request="uploadFile"
      :on-exceed="handleExceed"
    >
      <el-button slot="trigger" type="primary" class="upload"
        ><i class="el-icon-upload el-icon--left"></i>Add Data</el-button
      >
    </el-upload>
    <p>{{ fileName }}</p>
    <el-table
      ref="machineList"
      :data="fileList"
      highlight-current-row
      @current-change="handleCurrentChange"
      style="width: 100%"
    >
      <el-table-column type="index" width="50"> </el-table-column>
      <el-table-column property="name" label="fileList"> </el-table-column>
      <el-table-column label="opration">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
          >
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import axios from "axios";
import { EventBus } from "../event-bus.js";
export default {
  data() {
    return {
      fileName: "11",
      fileList: [],
      currentRow: null,
    };
  },
  methods: {
    // handleExceed(files, fileList) {
    handleExceed() {
      // this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`);
      this.$message.warning("当前限制选择 10 个文件");
    },
    uploadFile(fileObj) {
      // let formData = new FormData();
      let that = this;
      console.log(fileObj.file.name);
      // 把这行放到response200里
      that.fileList.push({ name: fileObj.file.name });
      // formData.set("file", fileObj.file);
      axios
        .post("http://127.0.0.1:5000/upload", fileObj.file.name, {
          headers: {
            "Content-Type": "text/plain",
          },
        })
        .then((response) => {
          if (response.status === 200) {
            // 提交成功将要执行的代码
            console.log('upload success')
            this.$message({
              message:'上传成功',
              type:'success'
            })
          }
        })
        .catch(function (error) {
          console.log(error);
          this.$message({
              message:'上传失败',
              type:'error'
          })
        });
    },
    handleCurrentChange(Row) {
      let that = this;
      that.currentRow = Row;
      EventBus.$emit('changeRow',that.currentRow.name)
    },
    handleEdit(index, row) {
      console.log(index, row);
    },
    handleDelete(index, row) {
      let that = this;
      this.fileList.splice(index,1);
      console.log(index, row);
    },
    getData() {
      axios
        .get("/get")
        .then((response) => {
          if (response.code === 200) {
            // 接受成功将要执行的代码
            console.log(response.data);
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    writeObj(obj){ 
      var description = ""; 
      for(var i in obj){ 
      var property=obj[i]; 
      description+=i+" = "+property+"\n"; 
      } 
    } 
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.upload {
  margin: 20px;
}
</style>