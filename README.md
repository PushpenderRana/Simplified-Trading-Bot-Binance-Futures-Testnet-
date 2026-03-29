# Simplified-Trading-Bot-Binance-Futures-Testnet-

It is a binance future testnet trading bot project using Django.
1.User Registration using django built-in user model and generate acess and refresh token
2. Then user login with their credentials.
3.Take a input from user for place a order and check the  validation of inputs(like price >0,quantitity>0) and store in Orders model
4.then call a Binance future  api for placing a order and if place then it's details save in Order's model

i have run the api on postman application where i check the login ,register , place order work properly
https://pushpenderrana270-2075325.postman.co/workspace/Pushpender-Rana's-Workspace~2f15070b-e327-41a0-8cc4-3a61723afb94/collection/51286070-df904a9d-7e4a-497d-b53f-20d562b56583?action=share&source=copy-link&creator=51286070

TECH STACK
-Python
-Django
-Django Rest Framework
-Binance API
-DBsqlite(database)
-Postman (for api testing
