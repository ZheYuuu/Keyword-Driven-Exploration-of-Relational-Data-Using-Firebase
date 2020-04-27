<template>
  <div>
    <div>Database:{{data_base}} Table:{{data_table}}</div>
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
  </div>
</template>
<script>
  // import reqwest from 'reqwest';
  import axios from 'axios';
  
  export default {
    props:["data_base", "data_table", "keyword", "entrys"],
    watch: { 
      data_table: function(newVal, oldVal) { 
        console.log("change datatable2!", newVal, oldVal);
        this.getData();
      },
      data_base: function(newVal, oldVal) { 
        console.log("change database2!", newVal, oldVal);
        this.getData();
      },
      // keyword: function(newVal, oldVal) {
      //   console.log("change keyword2!", newVal, oldVal);
      //   this.searchMode = true;
      //   this.showSearch(newVal);
      // }
    },
    mounted() {
      if (this.entrys.length > 0) {
        console.log("show entry!");
        this.showSearch();
      }
      else {
        console.log("get data!");
        this.getData();
      }
      
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
        // console.log('res', res);
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

      getPath(pk){
        if (pk != null) {
          return 'http://54.219.171.61:5000/api/' + this.data_base + '/' + this.data_table + '/' + pk;
        }
        else {
          return 'http://54.219.171.61:5000/api/' + this.data_base + '/' + this.data_table;
        }
      },

      getData() {
        const path = this.getPath(null);
        this.loading = true;
        // console.log(path);
        axios.get(path)
          .then((res) => {
            console.log(res);
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
      showSearch() {
        this.loading = true;
        let data = [];
        console.log("show entrys", this.entrys);
        for (let entry of this.entrys) {
          let path = this.getPath(entry);
          axios.get(path)
          .then((res) => {
            // console.log('entry', res);
            res.data['uuid'] = entry;
            data.push(res.data);
            // console.warn('data', data);
            if (data.length == this.entrys.length) {
              this.pagination = {
                total: data.length,
                current: 0,
                pageSize: 10
              };
              this.data = data;
              this.columns = this.getColumns(this.data);
              this.loading = false;
            }
          })
          .catch((error) => {
            console.error(error);
          })
        }
        // const path = this.getPath(search_word);
        // this.loading = true;
        // // console.log(path);
        // axios.get(path)
        //   .then((res) => {
        //     console.log(res);
        //     const metadata = res.data._meta;
        //     const pagination = {
        //       total: metadata.total_pages,
        //       current: 0,
        //       pageSize: 10
        //     };
        //   })
        //   .catch((error) => {
        //     console.error(error)
        //   });
      }
    },
  };
</script>
