let header = { 'Content-Type': 'application/json', "Access-Control-Allow-Origin":"*"}
let api_check = 'http://127.0.0.1:8000/progress_bar/?format=json'
let api_get_list = 'http://127.0.0.1:8000/test/api/get_list/?format=json'



new Vue({
    el:'#vue_app',
    data: {
        
        bar: 0,
        check_loop:"",
        polling:'',
        max: 10,
        text: ""


    },

    methods: {
        pollData () {
            this.polling = setInterval(() => {

                const vm = this
                axios
                      .get(api_check, headers = header)
                      .then(
              
                        response => {
                            vm.max = response.data.all
                            vm.bar = 100/response.data.all * response.data.current
                            document.getElementById("pr_bar").setAttribute("style","width: "+ this.bar+"%");
                            if(this.bar>99){
                                document.getElementById("pr_bar").setAttribute("style","display:none");

                            }

                        }
                          );
            }, 2000)

        },
    },
    beforeDestroy () {
        clearInterval(this.polling)
    },
    created () {
        this.pollData()
        
    },
})


var app = new Vue({
    el: "#vue_post",
    data: {
      file: '',
      e: ''
    },
    methods: {
      submitFile() {
        let formData = new FormData();
        formData.append('file', this.file);
        console.log('>> formData >> ', formData);
  
        // You should have a server side REST API 
        axios.post('http://127.0.0.1:8000/',
            formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'X-CSRFToken':document.getElementsByName("csrfmiddlewaretoken")[0].value
              }
            }
          ).then(
            response => {
                this.e = "В строке №" + response.data.row + " ошибка"
                if(response.data.success){
                    this.e = "Отправлено "+ response.data.row_count + " сертифика"
                }
            }
          )
          .catch(function () {
            console.log('FAILURE!!');
          });
      },
      handleFileUpload() {
        this.file = this.$refs.file.files[0];
        console.log('>>>> 1st element in files array >>>> ', this.file);
      }
    }
  });

