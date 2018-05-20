
<style>
    .bookfield {
        color:	#7B7B7B
        }
    
    .summary {
        margin-top: 100px
    }

</style>

<template>
    <div>
        <Card>
            <Row :gutter="16">
                <Col span='14'>
                    <Row>
                        <Col span='15'>
                            <img :src='imgsrc' style='max-width:450px'/>
                        </Col>
                        <Col span='8'>
                            <p><span class='bookfield'>书名: </span> {{obj.title}}</p>
                            <p><span class='bookfield'>出版社: </span> {{obj.publisher}}</p>
                            <p><span class='bookfield'>出版年: </span> {{obj.pubdate}}</p>
                            <p><span class='bookfield'>装帧: </span> {{obj.binding}}</p>
                            <p><span class='bookfield'>页数: </span> {{obj.pages}}</p>
                            <p><span class='bookfield'>定价: </span> {{obj.price}}</p>
                            <p><span class='bookfield'>作者: </span> {{obj.author}}</p>
                        </Col>

                    </Row>

                </Col>
                <Col span='8'>
                    <Alert>标签</Alert>
                    <span v-for="(item, index) in obj.tags" :key="index" >
                        <Tag checkable color="blue">{{item.name}}</Tag>
                    </span>
                    
                    <div class='summary'>
                        <Alert type="success">摘要</Alert>
                        {{obj.summary}}
                    </div>

                </Col>
            </Row>
        </Card>

    </div>
</template>
<script>
    export default {

        created () {  // 用created，显示不出图片
            this.getbooks()
        },

        data () {
            return {
                imgsrc:'',
                obj:'',
            }
        },

        methods: {

            getImg () {
                let imagepath = this.obj.image
                let impspl = imagepath.split('/')
                let imgname = impspl[impspl.length-1]
                this.imgsrc = 'http://myweb/image/' + imgname
            },

            getbooks () {
            const path = this.util.ajax.defaults.baseURL + this.backendsapi.doubanbook + this.$route.params.name 

            this.ajax({
                method: 'get',
                url: path,
                data: {},
            })

            .then(response => {
                console.log(response)
                this.obj = response.data.data.books[0]
                this.getImg()
            })

            .catch(error => {
                console.log(error)
            })

        },

        }



    }
</script>