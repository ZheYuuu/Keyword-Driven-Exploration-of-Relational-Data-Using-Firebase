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
  const columns = [
    {
      title: 'Date',
      dataIndex: 'date',
      // sorter: true,
      width: '20%',
      // scopedSlots: { customRender: 'name' },
    },
    {
      title: 'Area Code',
      dataIndex: 'area_code',
      // filters: [{ text: 'Male', value: 'male' }, { text: 'Female', value: 'female' }],
      width: '20%',
    },
    {
      title: 'Confirm',
      dataIndex: 'confirm',
    },
    {
      title: 'Death',
      dataIndex: 'death',
    },
    {
      title: 'Recover',
      dataIndex: 'recover',
    },
  ];

  export default {
    mounted() {
      // this.fetch();
      this.getData();
    },
    data() {
      return {
        data: [],
        pagination: {},
        loading: false,
        columns,
      };
    },
    methods: {
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
      getData() {
        const path = 'http://localhost:5000/api/coronavirus/daily_situation';
        axios.get(path)
          .then((res) => {
            const pagination = { ...this.pagination };
            const metadata = res.data._meta;
            pagination.total = metadata.total_pages;
            this.loading = false;
            this.data = this.getRecords(res);
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
        const path = 'http://localhost:5000/api/coronavirus/daily_situation';
        axios.get(path, { 
          params: params,
          })
          .then((res) => {
            this.data = this.getRecords(res);
            this.loading = false;
          })
          .catch((error)=>{
            console.error(error);
          });
        // reqwest({
        //   url: 'http://localhost:5000/api/coronavirus/daily_situation',
        //   method: 'get',
        //   data: {
        //     results: 10,
        //     ...params,
        //   },
        //   type: 'json',
        // }).then(data => {
        //   const pagination = { ...this.pagination };
        //   // Read total count from server
        //   // pagination.total = data.totalCount;
        //   pagination.total = 200;
        //   this.loading = false;
        //   this.data = data.results;
        //   console.log('view data', this.data);
        //   this.pagination = pagination;
        // });
      },
    },
  };
</script>
