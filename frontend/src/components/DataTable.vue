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
  import reqwest from 'reqwest';
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
      filters: [{ text: 'Male', value: 'male' }, { text: 'Female', value: 'female' }],
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
      getData() {
        const path = 'http://localhost:5000/Daily';
        axios.get(path)
          .then((res) => {
            // const pagination = { ...this.pagination };
            // // Read total count from server
            // // pagination.total = data.totalCount;
            // pagination.total = 200;
            // this.loading = false;
            this.data = res.data.data;
            console.log('view data', this.data);
            // this.pagination = pagination;
          })
          .catch((error) => {
            console.error(error);
          });
      },
      handleTableChange(pagination, filters, sorter) {
        console.log(pagination);
        const pager = { ...this.pagination };
        pager.current = pagination.current;
        this.pagination = pager;
        this.fetch({
          results: pagination.pageSize,
          page: pagination.current,
          sortField: sorter.field,
          sortOrder: sorter.order,
          ...filters,
        });
      },
      fetch(params = {}) {
        console.log('params:', params);
        this.loading = true;
        reqwest({
          url: 'http://127.0.0.1:5000/Daily',
          method: 'get',
          data: {
            results: 10,
            ...params,
          },
          type: 'json',
        }).then(data => {
          const pagination = { ...this.pagination };
          // Read total count from server
          // pagination.total = data.totalCount;
          pagination.total = 200;
          this.loading = false;
          this.data = data.results;
          console.log('view data', this.data);
          this.pagination = pagination;
        });
      },
    },
  };
</script>
