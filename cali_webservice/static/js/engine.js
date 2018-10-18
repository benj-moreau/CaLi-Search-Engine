var search = new Vue({
  el: '#search_engine',
  data: {
    licenses: {},
    selected_license: '',
    selected_license_label: null,
    selected_sens: 'compatible',
    query: ''
  },
  watch: {
    selected_license: function () {
      label = get_selected_license_label()
      if (label == 'License'){
        this.selected_license_label = null
      } else {
        this.selected_license_label = label;
      }
    }
  },
  mounted: function () {
    this.get_licenses();
  },
  methods: {
    get_licenses: function () {
      this.$http.get('/api/' + get_path_graph() + '/licenses/').then(response => {
        return response.body;
      }).then(json_licenses => {
        this.licenses = json_licenses;
      });
    },
    search: function () {
      parameters = "query=" + encodeURIComponent(this.query) + "&license=" + encodeURIComponent(this.selected_license.hashed_sets) + "&sens=" + encodeURIComponent(this.selected_sens);
      window.location = "/" + get_path_graph() + "/search?" + parameters
    },
  },
});

function get_selected_license_label() {
  return $("#license_selection option:selected").text();
}
