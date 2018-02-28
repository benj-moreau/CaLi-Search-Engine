var search_results = new Vue({
  el: '#search_results',
  data: {
    results: get_results(),
    nb_datasets: get_nb_datasets(),
    show_sets: false,
  },
});
