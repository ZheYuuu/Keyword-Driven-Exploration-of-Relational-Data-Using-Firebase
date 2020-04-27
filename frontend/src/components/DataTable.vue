<template>
  <a-table
    :columns="columns"
    :rowKey="record => record.uuid"
    :dataSource="data"
    :pagination="pagination"
    :loading="loading"
    @change="handleTableChange"
  >
    <!-- <template slot="name" slot-scope="name">
      {{name.first}} {{name.last}}
    </template> -->
  </a-table>
</template>
<script>
  // import reqwest from 'reqwest';
  import axios from 'axios';
  

  export default {
    props:["data_base", "data_table"],
    watch: { 
      data_table: function(newVal, oldVal) { 
        console.log("change!", newVal, oldVal);
        this.getData();
      },
      data_base: function(newVal, oldVal) { 
        console.log("change!", newVal, oldVal);
        this.getData();
      }
    },
    mounted() {
      // this.fetch();
      this.getData();
    },
    data() {
      let columns = [];
      return {
        data: [],
        pagination: {},
        loading: false,
        columns,
      };
    },
    methods: {
      getColumns(data) {
        let record = data[0];
        let columns = [];
        for (let k in record) {
          if (k!='uuid') {
            columns.push({
              title: k,
              dataIndex: k
            })
          }
        }
        return columns;
      },
      getRecords(res) {
        console.log('res', res);
        let items = res.data.items;
        let data = [];
        for (const pk in items) {
          let record = { uuid : pk };
          for (const k in items[pk]) {
            record[k] = items[pk][k];
          }
          data.push(record);
        }
        return data;
      },
      getPath(){
        let path = 'http://localhost:5000/api/' + this.data_base + '/' + this.data_table;
        return path;
      },
      getData() {
        const path = this.getPath();
        axios.get(path)
          .then((res) => {
            const metadata = res.data._meta;
            const pagination = {
              total: metadata.total_pages,
              current: 0,
              pageSize: 10
            };
            this.loading = false;
            this.data = this.getRecords(res);
            this.columns = this.getColumns(this.data);
            this.pagination = pagination;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      handleTableChange(pagination, filters, sorter) {
        // console.log('handle table', pagination);
        const pager = { ...this.pagination };
        pager.current = pagination.current;
        this.pagination = pager;

        this.fetch({
          page_size: pagination.pageSize,
          page: pagination.current - 1,
          sortField: sorter.field,
          sortOrder: sorter.order,
          ...filters,
        });
      },
      fetch(params = {}) {
        this.loading = true;
        const path = this.getPath(); 'http://localhost:5000/api/coronavirus/daily_situation';
        axios.get(path, { 
          params: params,
          })
          .then((res) => {
            this.data = this.getRecords(res);
            this.columns = this.getColumns(this.data);
            this.loading = false;
          })
          .catch((error)=>{
            console.error(error);
          });
      },
    },
  };
</script>
