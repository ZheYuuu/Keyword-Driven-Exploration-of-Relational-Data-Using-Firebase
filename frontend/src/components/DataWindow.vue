<template>
    <div id="databody">
        <div id="search-word">Search Keyword</div>
        <a-input-search placeholder="input search text" @search="onSearch" enterButton />
        <dataTable/>
    </div>
</template>

<script>
import dataTable from './DataTable.vue';
export default {
    name: 'dataWindow',
    components: {
        dataTable
    },
    methods: {
        onSearch(value) {
            console.log(value);
        }
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

