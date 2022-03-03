// Run event listeners upon loading page
document.addEventListener("DOMContentLoaded", function() {
    // Assigning hero image depending on page
    let hero = document.getElementsByClassName("hero-container");
    if (hero){
        let heroPageAttribute = hero[0].getAttribute("data-hero-page");
        switch (heroPageAttribute){
            case (heroPageAttribute = "home"):
                hero[0].style.background = "url('https://images.pexels.com/photos/2356045/pexels-photo-2356045.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260') no-repeat bottom/cover fixed";
                break;
            case heroPageAttribute = "article":
                hero[0].style.background = "url('https://images.pexels.com/photos/2662116/pexels-photo-2662116.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260') no-repeat bottom/cover fixed";
                break;
            case heroPageAttribute = "login":
                hero[0].style.background = "url('https://images.pexels.com/photos/2901209/pexels-photo-2901209.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260') no-repeat bottom/cover fixed";
                break;
            case heroPageAttribute = "signup":
                hero[0].style.background = "url('https://images.pexels.com/photos/2901209/pexels-photo-2901209.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260') no-repeat bottom/cover fixed";
                break;
            case heroPageAttribute = "logout":
                hero[0].style.background = "url('https://images.pexels.com/photos/2901209/pexels-photo-2901209.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260') no-repeat bottom/cover fixed";
                break;
        }
    }
})