<template>
  <div>
    <div>Database:{{data_base}} Table:{{data_table_name}}</div>
      <a-table
        :columns="columns"
        :rowKey="record => record.uuid"
        :dataSource="data"
        :pagination="pagination"
        :loading="loading"
        :scroll="{ x: 1000}"
        @change="handleTableChange"
      >
      <a slot="fk" slot-scope="text, record, tags, node" v-on:click="handleClick(text, record, tags, node)">{{ text }}</a>
    </a-table>
  </div>
</template>
<script>
  // import reqwest from 'reqwest';
  import axios from 'axios';

  const pk_map = {
    "city": ["ID"],
    "country": ["Code"],
    "countrylanguage": ["CountryCode", "Language"],
    "daily_situation": ["area_code", "date"],
    "statisic": ["date"],
    "area": ["area_code"],
    "train_info": ["ID"],
    "prov_railway_info": ["province"],
    "station_info": ["telecode"],
  };

  const fk_map = {
    "city": {"CountryCode": "country-Code"},
    "country": {},
    "countrylanguage": {"CountryCode": "country-Code"},
    "daily_situation": {"area_code": "area-area_code", "date": "statistic-date"},
    "statisic": {},
    "area": {},
    "train_info": {"start":"station_info-telecode", "end":"station_info-telecode"},
    "prov_railway_info": {},
    "station_info": {"province_pinyin": "prov_railway_info-province"},
  }
  
  export default {
    props:["data_base", "data_table", "keyword", "entrys"],
    watch: { 
      data_table: function(newVal, oldVal) { 
        console.log("change datatable2!", newVal, oldVal);
        this.data_table_name = this.data_table;
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
        // console.log("show entry!");
        this.showSearch();
      }
      else {
        // console.log("get data!");
        this.data_table_name = this.data_table;
        this.getData();
      }
      
    },
    data() {
      let columns = [];
      let data_table_name;
      return {
        data: [],
        pagination: {},
        loading: false,
        columns,
        data_table_name
      };
    },
    methods: {
      handleClick(text, record, tags, node) {
        // console.log("Click!", text, record, tags, node);
        let id = text;
        let fk = node.dataIndex;
        let out_obj = fk_map[this.data_table_name][fk].split('-');
        let new_table = out_obj[0];
        let path = this.getPath(id.toLowerCase(), new_table);
        this.data_table_name = new_table;
        axios.get(path)
        .then((res) => {
          console.log('click', res);
          res.data['uuid'] = id.toString();
          let data = res.data;
          this.pagination = {
            total: 1,
            current: 0,
            pageSize: 10
          };
          console.log('click', data);
          this.data = [data];
          this.columns = this.getColumns(this.data, new_table);
          
          this.loading = false;
          console.log("click Done.")
        })
        .catch((error) => {
          console.error(error);
        })
      },

      getColumns(data, table=this.data_table_name) {
        let record = data[0];
        let columns = [];
        let key_set = ['uuid'];
        console.log(pk_map, fk_map);
        
        // let base = this.data_base;
        // add pk
        for (let pk of pk_map[table]) {
          columns.push({
            title: pk,
            dataIndex: pk,
            // scopedSlots: { customRender: ['pk'] },
          });
          key_set.push(pk);
        }
        // add fk
        for (let fk in fk_map[table]) {
          // if it is also a pk
          if (key_set.indexOf(fk) != -1) {
            for (let i = 0; i < columns.length; i++) {
              if(columns[i]['title'] == fk) {
                columns[i]['scopeSlots'] = { customRender: 'fk' };
              }
            }
          }
          else {
            console.log(fk);
            columns.push({
              title: fk,
              dataIndex: fk,
              scopedSlots: { customRender: 'fk' },
            });
            key_set.push(fk);
          }
        }

        for (let k in record) {
          if (key_set.indexOf(k) == -1) {
              columns.push({
                title: k,
                dataIndex: k,
              });
          }
        }
        console.log("columns", columns);
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

      getPath(pk=null, table=null){
        if (table != null) {
          return 'http://54.219.171.61:5000/api/' + this.data_base + '/' + table + '/' + pk;
        }
        if (pk != null) {
          return 'http://54.219.171.61:5000/api/' + this.data_base + '/' + this.data_table_name + '/' + pk;
        }
        else {
          return 'http://54.219.171.61:5000/api/' + this.data_base + '/' + this.data_table_name;
        }
      },

      getData() {
        const path = this.getPath(null);
        this.loading = true;
        // console.log(path);
        axios.get(path)
          .then((res) => {
            // console.log(res);
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
            console.log("getData done.");
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
        console.warn("Im here!");

        this.fetch({
          page_size: pagination.pageSize,
          page: pagination.current - 1,
          sortField: sorter.field,
          sortOrder: sorter.order,
          ...filters,
        });
        console.log("handleChange done.");
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
            console.log("fetch done.");
          })
          .catch((error)=>{
            console.error(error);
          });
      },
      showSearch() {
        this.loading = true;
        let data = [];
        // console.warn("show entrys", this.entrys);
        for (let entry of this.entrys) {
          let path = this.getPath(entry);
          // console.warn("shw path", path);
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
      },
      
    },
  };
</script>

<style scoped>
  /* .is-pk {
    font-weight:bold; 
    text-decoration-line: underline;
  } */
</style>