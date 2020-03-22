<template>
  <div id="treebody">
    <a-tree :treeData="treeData" showIcon defaultExpandAll >
      <a-icon type="down" slot="switcherIcon" />
      <a-icon slot="database" theme="twoTone" type="database" />
      <a-icon slot="table" type="table" />
    </a-tree>
  </div>
</template>

<script>
  const treeData = [
    {
      title: 'World',
      key: '0-0',
      slots: {
        icon: 'database',
      },
      children: [
        { title: 'Area', key: '0-0-0', slots: { icon: 'table' } },
        { title: 'City', key: '0-0-1', scopedSlots: { icon: 'table' } },
        { title: 'Country', key: '0-0-2', scopedSlots: { icon: 'table' } },
        { title: 'Country Language', key: '0-0-3', scopedSlots: { icon: 'table' } },
      ],
    },
    {
      title: 'CoronaVirus',
      key: '0-1',
      slots: {
        icon: 'database',
      },
      children: [
        { title: 'Daily Release', key: '0-1-0', slots: { icon: 'table' } },
        { title: 'Coronavirus', key: '0-1-1', scopedSlots: { icon: 'table' } },
        { title: 'Area', key: '0-1-2', scopedSlots: { icon: 'table' } },
      ],
    },
    {
      title: 'China Train Network',
      key: '0-2',
      slots: {
        icon: 'database',
      },
      children: [
        { title: 'Train', key: '0-2-0', slots: { icon: 'table' } },
        { title: 'Province', key: '0-2-1', scopedSlots: { icon: 'table' } },
        { title: 'Station', key: '0-2-2', scopedSlots: { icon: 'table' } },
      ],
    }
  ];

  export default {
    data() {
      return {
        treeData,
      };
    },
    name: 'navigator',
    methods: {
      onSelect(selectedKeys, info) {
        console.log('selected', selectedKeys, info);
      },
      onCheck(checkedKeys, info) {
        console.log('onCheck', checkedKeys, info);
      },
    },
  };
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#treebody {
  text-align: left;
  flex-shrink:0;
  width: 30%;
}
</style>
