<style scoped>

</style>

<template>
  <div>
    <p> <span>动作：{{action}} </span> <span> , 类型：{{itemtype}} </span>  <span> , ids: {{targetids}} </span> </p>
    <Input icon="search" :placeholder="action" />
  </div>
</template>

<script>
export default {
  props: ['action', 'targetids', 'itemtype']
}
</script>
