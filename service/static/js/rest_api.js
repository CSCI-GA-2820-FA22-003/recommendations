$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#id").val(res.id);
        $("#product_1").val(res.product_1);
        $("#product_2").val(res.product_2);
        $("#recommendation_type").val(res.recommendation_type);
        if (res.liked == true) {
            $("#liked").val("true");
        } else {
            $("#liked").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#id").val("");
        $("#recommendation_type").val("");
        $("#product_1").val("");
        $("#product_2").val("");
        $("#liked").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {

        let recommendation_type = $("#recommendation_type").val();
        let product_1 = $("#product_1").val();
        let product_2 = $("#product_2").val();
        let liked = $("#liked").val() == "true";

        let data = {
            "id": 0,
            "recommendation_type": recommendation_type,
            "product_1": product_1,
            "product_2": product_2,
            "liked": liked
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/api/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        let id = $("#id").val();
        let recommendation_type = $("#recommendation_type").val();
        let product_1 = $("#product_1").val();
        let product_2 = $("#product_2").val();
        let liked = $("#liked").val() == "true";

        let data = {
            "id": id,
            "recommendation_type": recommendation_type,
            "product_1": product_1,
            "product_2": product_2,
            "liked": liked
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
                type: "PUT",
                url: `/api/recommendations/${id}`,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        let id = $("#id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/recommendations/${id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message("Not Found!")
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        let id = $("#id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/recommendations/${id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });


    // ****************************************
    // Like a Recommendation
    // ****************************************

    $("#like-btn").click(function () {

        let id = $("#id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/api/recommendations/${id}/like`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation liked!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    })

    // ****************************************
    // Dislike a Recommendation
    // ****************************************

    $("#dislike-btn").click(function () {

        let id = $("#id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/api/recommendations/${id}/like`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Recommendation disliked!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    })

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#pet_name").val();
        let category = $("#pet_category").val();
        let available = $("#pet_available").val() == "true";

        let recommendation_type = $("#recommendation_type").val();
        let product_1 = $("#product_1").val();
        let product_2 = $("#product_2").val();
        let liked = $("#liked").val() == "true";

        let queryString = ""

        if (recommendation_type) {
            queryString += 'recommendation_type=' + recommendation_type
        }
        if (product_1) {
            if (queryString.length > 0) {
                queryString += '&product_1=' + product_1
            } else {
                queryString += 'product_1=' + product_1
            }
        }
        if (product_2) {
            if (queryString.length > 0) {
                queryString += '&product_2=' + product_2
            } else {
                queryString += 'product_2=' + product_2
            }
        }
        if (liked) {
            if (queryString.length > 0) {
                queryString += '&liked=' + liked
            } else {
                queryString += 'liked=' + liked
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/api/recommendations?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Recommendation Type</th>'
            table += '<th class="col-md-2">Product 1</th>'
            table += '<th class="col-md-2">Product 2</th>'
            table += '<th class="col-md-2">liked</th>'
            table += '</tr></thead><tbody>'
            let firstRec = "";
            for(let i = 0; i < res.length; i++) {
                let rec = res[i];
                table +=  `<tr id="row_${i}"><td>${rec.id}</td><td>${rec.recommendation_type}</td><td>${rec.product_1}</td><td>${rec.product_2}</td><td>${rec.liked}</td></tr>`;
                if (i == 0) {
                    firstRec = rec;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstRec != "") {
                update_form_data(firstRec)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})