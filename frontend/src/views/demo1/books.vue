<style scoped>

  Input {
    margin-right:20px;
  }
  .topdistance {margin-top: 10px}
  .divleft {margin-left: 20px}
</style>

<template>
  <div>
    <Card>
    <div style="margin-top:10px;margin-bottom:10px">
      <Row>
        <Col span="4">
          <Input icon="search" v-model="search" @on-change="searchbooks" @on-click="searchbooks" @on-enter="searchbooks" placeholder="搜索" />
        </Col>
        <Col span="3">
          <div  style="float:right">
            <Button @click="addrelation" type="primary">创建</Button>
          </div>
        </Col>
      </Row>
    </div>
    <div>
      <Table :columns="columns1" :data="data1"></Table>
    </div>
    </br>
    <Page :total=total show-sizer :current=current @on-change="pagechange" @on-page-size-change="sizechange"></Page>

    <Modal
        v-model="modaledit"
        width="450"
        title="修改图书"
        ok-text="修改"
        @on-ok="editok"
        @on-cancel="editcancel">

        <Alert>图书信息</Alert>
        <Form ref="formedit" :model="formedit" :label-width="100">
          <FormItem label="书名：" prop="opinion">
            <Input v-model="formedit.name" ></Input>
          </FormItem>
          <FormItem label="价格：">
            <Input v-model="formedit.price"></Input>
          </FormItem>
          <FormItem label="备注：">
            <Input v-model="formedit.note"></Input>
          </FormItem>
        </Form>  

        <Row>
          <Alert>选择关联</Alert>
          <Col span="12">
          <div class='divleft'>
                <div style="border-bottom: 1px solid #e9e9e9;padding-bottom:6px;margin-bottom:6px;">
                    <Checkbox
                        :indeterminate="indeterminate"
                        :value="checkAll"
                        @click.prevent.native="edithandleCheckAll" @on-change="checkAllGroupChange">全选（用户）</Checkbox>
                </div>
                <Scroll height=200>
                  <CheckboxGroup v-model="editusers" @on-change="checkAllGroupChange">
                      <div v-for="(item, index) in userlist" :key="index" >
                        <Checkbox :label='item.id'>{{item.username}}</Checkbox>
                      </div>
                  </CheckboxGroup>
                </Scroll> 
          </div>
          </Col>
    
          <Col span="12">
          <div class='divleft'>
            <div style="border-bottom: 1px solid #e9e9e9;padding-bottom:6px;margin-bottom:6px;">
                <Checkbox
                    :indeterminate="groupindeterminate"
                    :value="groupcheckAll"
                    @click.prevent.native="groupedithandleCheckAll" @on-change="groupcheckAllGroupChange">全选（组）</Checkbox>
            </div>
          <Scroll height=200>
            <CheckboxGroup v-model="editgroups" @on-change="groupcheckAllGroupChange">
                <div v-for="(item, index) in grouplist" :key="index" >
                  <Checkbox :label='item.id'>{{item.name}}</Checkbox>
                </div>
            </CheckboxGroup>
          </Scroll>  
          </div>
          </Col>

        </Row>
    </Modal>

    <Modal
        v-model="modalcreate"
        title="创建图书"
        width="500"
        ok-text="创建"
        @on-ok="createbook"
        @on-cancel="cancel">

        <Alert> 图书信息 </Alert>
        <Form ref="formcreate" :model="formcreate" :rules="ruleValidate" :label-width="100">
          <FormItem label="书名：" prop="name">
            <Input v-model="formcreate.name" ></Input>
          </FormItem>
          <FormItem label="价格：" prop="price">
            <Input v-model="formcreate.price"></Input>
          </FormItem>
          <FormItem label="备注：" prop="note">
            <Input v-model="formcreate.note"></Input>
          </FormItem>
        </Form>  

        <Row>
          <Alert>选择关联</Alert>
          <Col span="12">
            <div class='divleft'>
              <div style="border-bottom: 1px solid #e9e9e9;padding-bottom:6px;margin-bottom:6px;">
                  <Checkbox
                      :indeterminate="indeterminate"
                      :value="checkAll"
                      @click.prevent.native="handleCheckAll" @on-change="checkAllGroupChange">全选（用户）</Checkbox>
              </div>
              <Scroll height=200>
                <CheckboxGroup v-model="checkAllGroup" @on-change="checkAllGroupChange">
                    <div v-for="(item, index) in userlist" :key="index" >
                      <Checkbox :label='item.id'>{{item.username}}</Checkbox>
                    </div>
                </CheckboxGroup>
              </Scroll>  
            </div>
          </Col>
    
          <Col span="12">
            <div class='divleft'>
              <div style="border-bottom: 1px solid #e9e9e9;padding-bottom:6px;margin-bottom:6px;">
                  <Checkbox
                      :indeterminate="groupindeterminate"
                      :value="groupcheckAll"
                      @click.prevent.native="grouphandleCheckAll" @on-change="groupcheckAllGroupChange">全选（组）</Checkbox>
              </div>
              <Scroll height=200>
                <CheckboxGroup v-model="groupcheckAllGroup" @on-change="groupcheckAllGroupChange">
                    <div v-for="(item, index) in grouplist" :key="index" >
                      <Checkbox :label='item.id'>{{item.name}}</Checkbox>
                    </div>
                </CheckboxGroup>
              </Scroll>  
            </div>
          </Col>
        </Row>


    </Modal>

    <Modal
        v-model="modaldeletebook"
        title="删除图书"
        @on-ok="deletebook"
        @on-cancel="cancel">
      <p>是否删除图书？</p>

    </Modal>

  </Card>
  </div>
</template>

<script>
import Vue from 'vue'
import {Icon, Button, Table, Modal, Page, Message} from 'iview';

export default {
  comments: {Icon, Button, Table, Modal, Page, Message},

  created () {
    this.getbooks()
    this.getusergroups(this.backendsapi.user, this.userlist, this.useridlist)
    this.getusergroups(this.backendsapi.group, this.grouplist, this.groupidlist)
  },

  data () {
    return {
      row:'',
      search:'',
      total:1,
      current:1,
      pagesize:10,
      modaledit:false,
      modalcreate:false,
      modaldeletebook:false,
      indeterminate: false,
      groupindeterminate: false,
      checkAll: false,
      groupcheckAll: false,
      userlist: [],
      useridlist: [], 
      checkAllGroup: [], 
      editusers: [], 
      grouplist: [],
      groupidlist: [],
      groupcheckAllGroup: [], 
      editgroups: [],
      formcreate: {
        name:'',
        note:'',
        price:'',
      },
      users:'',
      formedit:{
        name:'',
        price:'',
        note:'',
      },
      ruleValidate: {
        name: [{ required: true, message: '书名不能为空', trigger: 'blur' }],
        price: [{ required: true, message: '价格不能为空', trigger: 'blur' }],
        note: [{ required: true, message: '备注不能为空', trigger: 'blur' }],
      },
      data1:[],
      columns1: [
        {
          title: '书名',
          key: 'name',
          width: 150,
          render: (h, params) => {
            return h('router-link', {props:{to:'/demo1/book/'+params.row.name}},params.row.name)
          }
        },
        {
          title: '价格',
          key: 'price',
          width: 100,
          render: (h, params) => {
            return h('span', {},params.row.price + '元')
          }
        },
        {
          title: '备注',
          key: 'note',
          width: 150
        },
        {
          title: '用户',
          key: 'users',
          render: (h, params) => {
            let users = params.row.users
            let rendercontent = []
            if (users != []){
              for (let u in users){
                rendercontent.push(
                  h('Avatar', {
                    style:{
                      color: "#f56a00",
                      backgroundColor: "#fde3cf"
                    },
                  },users[u].name),
                )
              }
            }
            return h('div', [
              rendercontent
            ])
          }
        },     
        {
          title: '组',
          key: 'groups',
          render: (h, params) => {
            let groups = params.row.groups
            let rendercontent = []
            if (groups != []){
              for (let u in groups){
                rendercontent.push(
                  h('Tag', {
                    props:{color:'blue'},
                  },groups[u].name),
                )
              }
            }
            return h('div', [
              rendercontent
            ])
          }
        }, 

        {
          title: '优惠',
          key: 'Ifname',
          width: 60,
          align: 'center',
          render: (h, params) => {
            if (params.row.price < 50) {
              return h('div', [h(Icon,{props:{type:'checkmark'}},)])
            } else {
              return h('div', [h(Icon,{props:{type:'close'}},)])
            }
          },
        },
        {
          title: '操作',
          key: 'action',
          width: 150,
          align: 'center',
          render: (h, params) => {
            return h('div', [
              h(Button, {
                  props: {
                    type: 'warning',
                    size: 'small'
                  },
                  style: {
                    marginRight: '12px'
                  },
                  on: {
                    click: () => {
                      this.modaledit = true
                      this.row = params.row
                      this.formedit.name = params.row.name
                      this.formedit.note = params.row.note
                      this.formedit.price = params.row.price
                      let users = params.row.users
                      let groups = params.row.groups
                      this.editusers = []
                      for (let u in users){
                        this.editusers.push(users[u].id)
                      }
                      this.editgroups = []
                      for (let g in groups){
                        this.editgroups.push(groups[g].id)
                      }
                      this.checkAllGroupChange(this.editusers)
                      this.groupcheckAllGroupChange(this.editgroups)
                    }
                  }
              }, '修改'),
              h(Button, {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.modaldeletebook = true
                    this.row = params.row
                  }
                }
              }, '删除')
            ])
          }
        },

      ],

    }
  },
  
  methods: {
      editok () {
        this.editbook (this.row.id)
        Message.info('Clicked ok');
      },

      addrelation() {
        this.modalcreate = true
        this.checkAll = false
        this.groupcheckAll = false
      },

      editcancel (){
        Message.info('Clicked cancel');
      },

      ok () {
        this.$Message.info('Clicked ok');
      },

      cancel () {
        this.$Message.info('Clicked cancel');
      },

      success (nodesc, title, ) {
          this.$Notice.success({
              title: title,
          });
      },

      getbooks () {
        const path = this.util.ajax.defaults.baseURL + this.backendsapi.book + '?page=' + this.current + '&pagesize=' + this.pagesize + '&search=' + this.search

        this.ajax({
          method: 'get',
          url: path,
          data: {},
        })

        .then(response => {
          console.log(response)
          this.data1 = response.data.results
          this.total = response.data.count
        })

        .catch(error => {
          console.log(error)
        })

      },

      getusergroups (uri, objlist, objidlist) {
        const path = this.util.ajax.defaults.baseURL + uri + '?page=' + this.current + '&pagesize=' + this.pagesize

        this.ajax({
          method: 'get',
          url: path,
          data: {},
        })

        .then(response => {
          let results = response.data.results
          for (let i in results){
            objidlist.push(results[i].id)
            objlist.push(results[i])
          }
        })

        .catch(error => {
          console.log(error)
        })

      },

      createbook () {
        const path = this.util.ajax.defaults.baseURL + this.backendsapi.book

        this.ajax({
          method: 'post',
          url: path,
          data: {name:this.formcreate.name, note:this.formcreate.note, price:this.formcreate.price, users:this.checkAllGroup, groups:this.groupcheckAllGroup},
        })

        .then(response => {
          let title = this.formcreate.name + ' 创建成功'
          this.success(true, title);
          this.getbooks()
        })

        .catch(error => {
          console.log(error)
        })
      },

      deletebook () {
        let id = this.row.id
        const path = this.util.ajax.defaults.baseURL + this.backendsapi.book + id + '/'

        this.ajax({
          method: 'delete',
          url: path,
          data: {},
        })

        .then(response => {
          let title = this.row.name + ' 删除成功'
          this.success(true, title);
          this.getbooks()
        })

        .catch(error => {
          console.log(error.response)
        })
      },

      editbook (id) {
        const path = this.util.ajax.defaults.baseURL + this.backendsapi.book + id + '/'

        this.ajax({
          method: 'patch',
          url: path,
          data: {name:this.formedit.name,price:this.formedit.price, note:this.formedit.note, users:this.editusers, groups:this.editgroups},
        })

        .then(response => {
          let title = this.formedit.name + ' 修改成功'
          this.success(true, title);
          this.getbooks()
        })

        .catch(error => {
          console.log(error.response)
        })
      },

      handleCheckAll (data) {
        if (this.indeterminate) {
            this.checkAll = false;
        } else {
            this.checkAll = !this.checkAll;
        }
        this.indeterminate = false;

        if (this.checkAll) {
            this.checkAllGroup = this.useridlist;
        } else {
            this.checkAllGroup = [];
        }
      },

      edithandleCheckAll (data) {
        if (this.indeterminate) {
            this.checkAll = false;
        } else {
            this.checkAll = !this.checkAll;
        }
        this.indeterminate = false;

        if (this.checkAll) {
            this.editusers = this.useridlist;
        } else {
            this.editusers = [];
        }
      },

      checkAllGroupChange (data) {
        if (data.length === this.userlist.length) {
            this.indeterminate = false;
            this.checkAll = true;
        } else if (data.length > 0) {
            this.indeterminate = true;
            this.checkAll = false;
        } else {
            this.indeterminate = false;
            this.checkAll = false;
        }
      },

      grouphandleCheckAll (data) {
        if (this.groupindeterminate) {
            this.groupcheckAll = false;
        } else {
            this.groupcheckAll = !this.groupcheckAll;
        }
        this.groupindeterminate = false;

        if (this.groupcheckAll) {
            this.groupcheckAllGroup = this.groupidlist;
        } else {
            this.groupcheckAllGroup = [];
        }
      },

      groupedithandleCheckAll (data) {
        if (this.groupindeterminate) {
            this.groupcheckAll = false;
        } else {
            this.groupcheckAll = !this.groupcheckAll;
        }
        this.groupindeterminate = false;

        if (this.groupcheckAll) {
            this.editgroups = this.groupidlist;
        } else {
            this.editgroups = [];
        }
      },

      groupcheckAllGroupChange (data) {
        if (data.length === this.grouplist.length) {
            this.groupindeterminate = false;
            this.groupcheckAll = true;
        } else if (data.length > 0) {
            this.groupindeterminate = true;
            this.groupcheckAll = false;
        } else {
            this.groupindeterminate = false;
            this.groupcheckAll = false;
        }
      },

      pagechange (page) {
        this.current = page
        this.getbooks()
      },

      sizechange(size){
        this.pagesize = size
        this.getbooks()
      },

      searchbooks(){
        this.current = 1
        this.getbooks()
      }

  },

}
</script>
