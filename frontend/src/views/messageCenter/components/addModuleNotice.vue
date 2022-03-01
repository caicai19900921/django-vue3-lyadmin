<template>
    <div v-dialogDrag>
    <el-dialog
            :title="loadingTitle"
            v-model="dialogVisible"
            width="50%"
            center
            :destroy-on-close="true"
            :close-on-click-modal="false"
            :before-close="handleClose">
        <el-form :inline="false" :model="formData" :rules="rules" ref="rulesForm" label-position="right" label-width="130px">
            <el-form-item label="公告标题：" prop="msg_title">
                <el-input type="text" v-model.trim="formData.msg_title" style="width: 300px"></el-input>
            </el-form-item>
            <el-form-item label="跳转路径：" prop="to_path">
                <el-input type="text" v-model.trim="formData.to_path" style="width: 300px"></el-input>
            </el-form-item>
            <el-form-item label="公告内容：" prop="msg_content">
<!--                <el-input type="textarea" v-model.trim="formData.name" style="width: 300px"></el-input>-->
                <div>
                    <TEditor v-model="formData.msg_content" ></TEditor>
                </div>
            </el-form-item>
            <el-form-item label="是否发布：" prop="status">
                <el-switch
                        v-model="formData.status"
                        active-color="#13ce66"
                        inactive-color="#ff4949">
                </el-switch>
            </el-form-item>
        </el-form>
        <span slot="footer">
            <el-button @click="handleClose" :loading="loadingSave">取消</el-button>
            <el-button type="primary" @click="submitData" :loading="loadingSave">确定</el-button>
        </span>
    </el-dialog>
    </div>
</template>

<script>
    import {messagesMessagenoticeAdd,messagesMessagenoticeEdit} from "@/api/api";
    import TEditor from '@/components/TEditor'
    export default {
        components: { TEditor },
        emits: ['refreshData'],
        name: "addModuleNotice",
        data() {
            return {
                dialogVisible:false,
                loadingSave:false,
                loadingTitle:'',
                formData:{
                    msg_title:'',
                    to_path:'',
                    msg_content:'',
                    status:true
                },
                rules:{
                    msg_title: [
                        {required: true, message: '请填写公告标题',trigger: 'blur'}
                    ],
                    msg_content: [
                        {required: true, message: '请填写公告内容',trigger: 'blur'}
                    ]
                }
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
                    msg_title:'',
                    to_path:'',
                    msg_content:'',
                    status:true
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
                            messagesMessagenoticeEdit(param).then(res=>{
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
                            messagesMessagenoticeAdd(param).then(res=>{
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

<style>
    .set-specs .el-form-item__content{
        background: #e6e6e6 !important;
    }
</style>

