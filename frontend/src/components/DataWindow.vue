<template>
    <div id="databody">
        <div id="search-word">Search Keyword</div>
        <a-input-search placeholder="input search text" @search="onSearch" enterButton ref="search_box" v-model="search_input"/>
        <dataTable v-bind:key="table.data_table" v-bind:data_base="table.data_base" v-bind:data_table="table.data_table" v-bind:keyword="table.keyword" v-bind:entrys="table.entrys" v-for="table in tables"/>
    </div>
</template>

<script>
import dataTable from './DataTable.vue';
import axios from 'axios';

export default {
    name: 'dataWindow',
    props: ["data_base", "data_table"],
    watch: {
        data_table: function(newVal, oldVal) { 
            console.log("change datatable1!", newVal, oldVal);
            this.tables = [{
                data_base: this.data_base,
                data_table: this.data_table,
                keyword: "",
                entrys: []
            }];
            this.search_input = "";
            // console.log(this.$refs.search_box);
            // document.getElementById('search_box').value = "";
        },
        data_base: function(newVal, oldVal) { 
            console.log("change database1!", newVal, oldVal);
            this.tables = [{
                data_base: this.data_base,
                data_table: this.data_table,
                keyword: "",
                entrys: []
            }]
            this.search_input = "";
            // document.getElementById('search_box').value = "";
        },
    },
    components: {
        dataTable
    },
    data() {
        let tables = [{
            data_base: this.data_base,
            data_table: this.data_table,
            keyword: "",
            entrys: []
        }];
        let search_input = "";
        return {tables, search_input};
    },
    methods: {
        sortData(items) {
            let table_entrys = {};
            for (let item of items) {
                let table_name = item['table'];
                if (table_name in table_entrys) {
                    table_entrys[table_name].push(item['pk']);
                }
                else {
                    table_entrys[table_name] = [item['pk']];
                }
            }
            return table_entrys;
        },
        onSearch(value) {
            let path = 'http://54.219.171.61:5000/api/' + this.data_base + '/index?keyword=' + value;
            axios.get(path)
                .then((res) => {
                    // console.log(res);
                    this.tables = [];
                    let table_entrys = this.sortData(res.data);
                    for (let table_name in table_entrys) {
                        let table = {
                            data_base: this.data_base,
                            data_table: table_name,
                            keyword: value,
                            entrys: table_entrys[table_name]
                        }
                        this.tables.push(table);
                        break;
                    }
                    console.log("tables", this.tables);
                })
                .catch((error) => {
                    console.error(error);
                })
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

