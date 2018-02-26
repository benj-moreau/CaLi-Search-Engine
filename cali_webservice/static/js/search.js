var search_results = new Vue({
  el: '#search_results',
  data: {
    results: {},
    hashed_set: '',
    selected_sens: '',
    query: ''
  },
  mounted: function () {
    this.get_results();
  },
  methods: {
    get_results: function () {
      /*
      this.$http.get('/api/licenses/').then(response => {
        return response.body;
      }).then(json_licenses => {
        this.licenses = json_licenses;
      });
      */
    },
  },
});
