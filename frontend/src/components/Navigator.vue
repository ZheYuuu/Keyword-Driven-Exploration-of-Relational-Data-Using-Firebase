<template>
  <div id="wholespace">
    <div id="treebody">
      <a-tree :treeData="treeData" showIcon defaultExpandAll @select="onSelect" :defaultSelectedKeys="['0-0-0']">
        <a-icon type="down" slot="switcherIcon" />
        <a-icon slot="database" theme="twoTone" type="database" />
        <a-icon slot="table" type="table"/>
      </a-tree>
    </div>
    <div id="seperator"></div>
    <dataWindow v-bind:data_base="data_base" v-bind:data_table="data_table"/>
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
        // { title: 'Area', key: '0-0-0', slots: { icon: 'table' } },
        { title: 'City', key: '0-0-0', scopedSlots: { icon: 'table' } },
        { title: 'Country', key: '0-0-1', scopedSlots: { icon: 'table' } },
        { title: 'Country Language', key: '0-0-2', scopedSlots: { icon: 'table' } },
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
  import dataWindow from './DataWindow.vue';
  // import dataTable from './DataTable.vue';
  const data_base_map = {
    "World": {
      data_base: "world",
      data_table_map: {
        "City": "city",
        "Country": "country",
        "Country Language": "countrylanguage",
      }
    },
    "CoronaVirus": {
      data_base: "coronavirus",
      data_table_map: {
        "Daily Release": "daily_situation",
        "Coronavirus": "statisic",
        "Area": "area",
      }
    },
    "China Train Network":{
      data_base: "china_train",
      data_table_map: {
        "Train": "train_info",
        "Province": "prov_railway_info",
        "Station": "station_info",
      }
    }
  };

  export default {
    data() {
      let data_base = "world";
      let data_table = "city";
      // let shift = false;
      return {
        treeData,
        data_base,
        data_table,
      };
    },

    components: {
      dataWindow
    },
    name: 'navigator',

    methods: {
      onSelect(selectedKeys, info) {
        let data_base_title= info.node.$parent.title;
        if (data_base_title in data_base_map) {
          let data_table_title = info.node.title;
          let data_table_map = data_base_map[data_base_title]["data_table_map"];
          if (data_table_title in data_table_map) {
            this.data_base = data_base_map[data_base_title]["data_base"];
            this.data_table = data_table_map[data_table_title];
            // this.shift = !this.shift;
          }
        }
      },

      // onCheck(checkedKeys, info) {
      //   console.log('onCheck', checkedKeys, info);
      // },
    },
  };
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#treebody {
  text-align: left;
  flex-shrink:0;
  width: 25%;
}

#seperator {
  width: 1em;
  border: #2c3e50 2px;
  box-shadow: 2px;
}

#wholespace {
  /* width:100%; */
  display: flex;
}

</style>
