// Run event listeners upon loading page
document.addEventListener("DOMContentLoaded", function() {
    // Assigning hero image depending on page
    let hero = document.getElementsByClassName("hero-container");
    if (hero){
        let heroPageAttribute = hero[0].getAttribute("data-hero-page");
        switch (heroPageAttribute){
            case heroPageAttribute = "home":
                hero[0].style.backgroundImage = "url('https://images.pexels.com/photos/2901209/pexels-photo-2901209.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')";
            case heroPageAttribute = "article":
                hero[0].style.backgroundImage = "url('https://images.pexels.com/photos/2901209/pexels-photo-2901209.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260')";
        }
    }
})