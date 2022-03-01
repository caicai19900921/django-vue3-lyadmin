<template>
    <div v-dialogDrag>
    <el-dialog
            :title="loadingTitle"
            v-model="dialogVisible"
            width="50%"
            center
            top="1%"
            :destroy-on-close="true"
            :close-on-click-modal="false"
            :before-close="handleClose">
        <el-form :inline="false" :model="formData" :rules="rules" ref="rulesForm" label-position="right" label-width="130px">
            <!--<el-form-item label="图片：" prop="image">-->
<!--&lt;!&ndash;                <img src="" style="width: 60px;height:60px">&ndash;&gt;-->

                <!--<el-upload-->
                        <!--class="avatar-uploader"-->
                        <!--:limit="1"-->
                        <!--action=""-->
                        <!--:show-file-list="false"-->
                        <!--:http-request="imgUploadRequest"-->
                        <!--:on-success="imgUploadSuccess"-->
                        <!--:before-upload="imgBeforeUpload">-->
                    <!--<img v-if="formData.image" :src="formData.image" class="avatar">-->
                    <!--<i v-else class="el-icon-plus avatar-uploader-icon"></i>-->
                <!--</el-upload>-->
            <!--</el-form-item>-->



            <el-form-item label="名称：" prop="name">
                <el-input v-model.trim="formData.name" style="width: 300px"></el-input>
            </el-form-item>
            <el-form-item label="排序：" prop="sort">
                <el-input-number v-model="formData.sort"  :min="1" :max="9999"></el-input-number>
            </el-form-item>
            <el-form-item label="键名：" prop="key">
                <el-input v-model.trim="formData.key" style="width: 300px" :disabled="loadingTitle=='编辑'"></el-input>
                <span style="color: red;font-size: 10px;margin-left: 8px">提示：该项添加后不能修改</span>
            </el-form-item>
            <el-form-item label="类型：">
                <el-radio-group v-model="type">
                    <el-radio label="1">正常</el-radio>
                    <el-radio label="2">富文本</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="" v-if="type==2">
                <div>
                    <TEditor v-model="formData.value" ></TEditor>
                </div>
            </el-form-item>
            <el-form-item label="键值：" prop="value" v-if="type==1">
                <el-input v-model.trim="formData.value" style="width: 300px"></el-input>
            </el-form-item>
            <el-form-item label="状态：" prop="status">
                <el-switch
                        v-model="formData.status"
                        active-color="#13ce66"
                        inactive-color="#ff4949">
                </el-switch>
            </el-form-item>

        </el-form>
        <template #footer>
            <el-button @click="handleClose" :loading="loadingSave">取消</el-button>
            <el-button type="primary" @click="submitData" :loading="loadingSave">确定</el-button>
        </template>
    </el-dialog>
    </div>
</template>

<script>
    import {platformsettingsOtherAdd,platformsettingsOtherEdit} from "@/api/api";
    import TEditor from '@/components/TEditor'
    export default {
        components: { TEditor },
        emits: ['refreshData'],
        name: "addModuleOther",
        data() {
            return {
                type:'1',
                isClear: false,
                dialogVisible:false,
                loadingSave:false,
                loadingTitle:'',
                formData:{
                    name:'',
                    key:'',
                    value:'',
                    sort:'',
                    status:true,
                },
                rules:{
                    name: [
                        {required: true, message: '请输入名称',trigger: 'blur'}
                    ],
                    key: [
                        {required: true, message: '请输入键名',trigger: 'blur'}
                    ],
                    value: [
                        {required: true, message: '请输入键值',trigger: 'blur'}
                    ],
                },
            }
        },
        methods:{

            handleClose() {
                this.dialogVisible=false
                this.loadingSave=false
                this.$emit('refreshData')
            },
            addModuleFn(item,flag) {
                this.loadingTitle=flag
                this.dialogVisible=true
                this.formData=item ? item : {
                    name:'',
                    key:'',
                    value:'',
                    sort:'',
                    status:true,
                }

            },
            submitData() {
                this.$refs['rulesForm'].validate(obj=>{
                    if(obj) {
                        this.loadingSave=true
                        let param = {
                            ...this.formData
                        }
                        if(this.formData.id){
                            platformsettingsOtherEdit(param).then(res=>{
                                this.loadingSave=false
                                if(res.code ==2000) {
                                    this.$message.success(res.msg)
                                    this.handleClose()
                                    this.$emit('refreshData')
                                } else {
                                    this.$message.warning(res.msg)
                                }
                            })
                        }else{
                            platformsettingsOtherAdd(param).then(res=>{
                                this.loadingSave=false
                                if(res.code ==2000) {
                                    this.$message.success(res.msg)
                                    this.handleClose()
                                    this.$emit('refreshData')
                                } else {
                                    this.$message.warning(res.msg)
                                }
                            })
                        }

                    }
                })
            },
        }
    }
</script>
