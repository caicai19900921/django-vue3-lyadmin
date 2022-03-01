/**
* 头部菜单
*/
<template>
  <el-menu class="el-menu-demo" mode="horizontal" background-color="#3C444D" text-color="#ffffff" active-text-color="#ffffff">

      <li class="logobox" :style="collapsed ? 'width:160px' : 'width:64px;margin-left:0'">
        <img class="logoimg" src="../assets/img/logo.png" alt="">
      </li>
      <el-button class="buttonimg">
        <img class="showimg" :src="collapsed?imgsq:imgshow" @click="toggle(collapsed)">
      </el-button>
      <el-row style="float: right;">
        <span style="line-height: 60px;align-items: center;padding-right: 10px;cursor: pointer;" @click="fullScreen">
            <el-tooltip
            class="box-item"
            effect="dark"
            content="全屏"
            placement="bottom">
        <el-icon style="font-size: 16px;color: white;"><full-screen /></el-icon>
      </el-tooltip>
        </span>
        <el-sub-menu index="2" class="submenu" style="width:auto;">
          <template #title>你好,{{userName}}</template>
          <el-menu-item @click="exit()">退出</el-menu-item>
        </el-sub-menu>
      </el-row>

  </el-menu>
</template>
<script>
  import screenfull from 'screenfull'
  export default {
    name: 'navcon',
    data() {
      return {
        userType:sessionStorage.getItem('userType'),
        studioId: parseInt(sessionStorage.getItem('studioId')),
        collapsed: true,
        imgshow: require('../assets/img/show.png'),
        imgsq: require('../assets/img/sq.png'),
        userName: ''
      }
    },
    // 创建完毕状态(里面是操作)
    created() {
      let userName = sessionStorage.getItem('userName')
      this.userName=userName
    },
    methods: {
      // 退出登录
      exit() {
        this.$confirm('退出登录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            this.$store.commit('logout', 'false')
            this.$router.push({path: '/login'})
            sessionStorage.clear()
            this.$message.success('已退出登录!')
          })
          .catch(() => {
          })
      },
      // 切换显示
      toggle(showtype) {
        this.collapsed = !showtype
        this.$Bus.emit('toggle', this.collapsed)
      },
      //全屏显示
      fullScreen () {
        if (!screenfull.isEnabled) {
          this.$message({
            message: '您的浏览器不支持全屏',
            type: 'warning'
          })
          return false
        }
        screenfull.toggle()
      },
    }
  }
</script>
<style lang="scss" scoped>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    border: none;
  }
  .submenu {
    float: right;
    .el-sub-menu__title{
      border-bottom: 0 !important;
      border-bottom-color: transparent !important;
    }
  }
  .is-console{
    float: right;
    margin: 14px;
  }

  .buttonimg {
    height: 60px;
    background-color: transparent;
    border: none;
    position: relative;
    float: left;
  }

  .showimg {
    width: 26px;
    height: 26px;
    position: absolute;
    top: 17px;
    left: 0;
  }

  .showimg:active {
    border: none;
  }

  .logobox {
    height: 40px;
    line-height: 40px;
    color: #9d9d9d;
    font-size: 20px;
    text-align: center;
    margin-left: 20px;
    display: inline-block;
    outline: none;
    float: left;
  }
  .logoimg {
    height: 40px;
  }
  .el-menu-demo{
    display: block
  }
</style>
<style>
  .submenu .el-submenu__title{
       border-bottom: 0 !important;
       border-bottom-color: transparent !important;
    }

  /*菜单关闭*/
  .submenu>.el-sub-menu__title .el-sub-menu__icon-arrow{
      position: unset;
  }
  /*菜单展开*/
  .submenu.is-opened>.el-sub-menu__title .el-sub-menu__icon-arrow{
      position: unset;
  }

</style>