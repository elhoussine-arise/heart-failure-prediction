$(document).ready(function() {
    $("#makePred").click(function() {
        console.log("Bouton 'Run Model' cliqué");
        
        // Effacer les anciens résultats
        $("#hfProb").empty();
        $("#hfPlot").empty();

        // Vérifier si les éléments existent
        if($("#hfProb").length === 0 || $("#hfPlot").length === 0) {
            console.error("Erreur: Les éléments #hfProb ou #hfPlot sont introuvables dans index.html !");
            return;
        }

        // Récupérer les valeurs des champs du formulaire et s'assurer qu'ils sont au bon format
        var inputData = {
            'age': Number($("#age").val()),
            'anaemia': Number($("#anaemia").val()),
            'creatinine_phosphokinase': Number($("#creatinine_phosphokinase").val()),
            'diabetes': Number($("#diabetes").val()),
            'ejection_fraction': Number($("#ejection_fraction").val()),
            'high_blood_pressure': Number($("#high_blood_pressure").val()),
            'platelets': Number($("#platelets").val()),
            'serum_creatinine': Number($("#serum_creatinine").val()),
            'serum_sodium': Number($("#serum_sodium").val()),
            'sex': Number($("#sex").val()),
            'smoking': Number($("#smoking").val()),
            'time': Number($("#time").val())
        };
        
        console.log("Données envoyées à l'API:", JSON.stringify(inputData));
        
        $.ajax({
            type: "POST",
            url: "/main/api/make_prediction",
            contentType: "application/json",
            data: JSON.stringify(inputData),
            dataType: "json",
            success: function(response) {
                console.log("Réponse de l'API reçue:", response);
                
                if (response.error) {
                    console.error("Erreur renvoyée par l'API:", response.error);
                    $("#hfProb").html("<p style='color: red;'>Erreur de l'API: " + response.error + "</p>");
                    return;
                }
                
                if (typeof response.probability === 'undefined' || !response.shap_plots) {
                    console.error("Réponse incomplète de l'API", response);
                    $("#hfProb").html("<p style='color: red;'>Réponse incomplète reçue.</p>");
                    return;
                }
                
                // Affiche la probabilité sous forme de pourcentage
                $("#hfProb").html("<h4>Predicted Risk: " + (response.probability * 100).toFixed(2) + "%</h4>");
                
                // Construction du contenu HTML pour afficher les deux graphiques SHAP
                var waterfall_img = response.shap_plots.waterfall_plot;
                var summary_img = response.shap_plots.summary_plot;
                var htmlContent = "<h5>Waterfall Plot</h5><img src='" + waterfall_img + "' width='500'/><br/>";
                htmlContent += "<h5>Summary Plot</h5><img src='" + summary_img + "' width='500'/>";
                $("#hfPlot").html(htmlContent);
                
                console.log("Images SHAP affichées dans #hfPlot");
            },
            error: function(err) {
                console.error("Erreur lors de l'appel API:", err);
                $("#hfProb").html("<p style='color: red;'>Une erreur est survenue lors de la requête.</p>");
            }
        });
        $("#resultsCard").fadeOut(100, function() {
            $(this).fadeIn(300);
        });
    });
});
