<template>
    <div id="databody">
        <div id="search-word">Search Keyword</div>
        <a-input-search placeholder="input search text" @search="onSearch" enterButton />
        <dataTable v-bind:data_base="data_base" v-bind:data_table="data_table"/> <!-- v-bind:columns="columns"/> -->
    </div>
</template>

<script>
import dataTable from './DataTable.vue';
export default {
    name: 'dataWindow',
    props: ["data_base", "data_table"],
    // data() {
    //     const columns = [
    //     {
    //         title: 'Date',
    //         dataIndex: 'date',
    //         width: '20%',
    //     },
    //     {
    //         title: 'Area Code',
    //         dataIndex: 'area_code',
    //         width: '20%',
    //     },
    //     {
    //         title: 'Confirm',
    //         dataIndex: 'confirm',
    //     },
    //     {
    //         title: 'Death',
    //         dataIndex: 'death',
    //     },
    //     {
    //         title: 'Recover',
    //         dataIndex: 'recover',
    //     },
    //     ];
    //     return {
    //         columns
    //     }
    // },
    components: {
        dataTable
    },
    methods: {
        onSearch(value) {
            console.log(value);
        },
    }
}
</script>

<style scoped>
#databody {
    width: 65%;
    flex-shrink:0;
}

#search-word {
    text-align: left;
    color: dimgray;
    margin-bottom: 2px;
}

</style>

