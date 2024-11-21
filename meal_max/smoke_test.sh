#!/bin/bash

# Base URL for meal_max API
BASE_URL="http://localhost:5001/api"
ECHO_JSON=false

# Option to echo JSON responses for debugging
if [[ "$1" == "--echo-json" ]]; then
  ECHO_JSON=true
fi

# Function to print JSON responses if ECHO_JSON is enabled
print_json() {
  if $ECHO_JSON; then
    echo "$1" | jq .
  fi
}

# Health Check Functions
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}


# Meal Management Functions
clear_meals() {
  echo "Clearing all meals from catalog..."
  curl -s -X DELETE "$BASE_URL/meals" > /dev/null
}

create_meal() {
  local data="$1"
  echo "Creating meal: $data"
  response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "$BASE_URL/meals")
  print_json "$response"
}

get_all_meals() {
  echo "Retrieving all meals..."
  response=$(curl -s "$BASE_URL/meals")
  print_json "$response"
}

delete_meal_by_id() {
  local meal_id="$1"
  echo "Deleting meal with ID: $meal_id"
  curl -s -X DELETE "$BASE_URL/meals/$meal_id" > /dev/null
}

# Battle Management Functions
prepare_battle() {
  local data="$1"
  echo "Preparing combatants for battle: $data"
  response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" "$BASE_URL/battle/prep")
  print_json "$response"
}

start_battle() {b
  echo "Starting battle..."
  response=$(curl -s -X POST "$BASE_URL/battle/start")
  print_json "$response"
}

clear_battles() {
  echo "Clearing all battles..."
  curl -s -X POST "$BASE_URL/battle/clear" > /dev/null
}

get_battle_stats() {
  echo "Retrieving battle statistics..."
  response=$(curl -s "$BASE_URL/battle/stats")
  print_json "$response"
}

# Kitchen Management Functions
update_meal_stats() {
  local meal_id="$1"
  local stat_type="$2"
  echo "Updating stats for meal ID: $meal_id, type: $stat_type"
  response=$(curl -s -X PUT "$BASE_URL/kitchen/update/$meal_id/$stat_type")
  print_json "$response"
}

get_kitchen_inventory() {
  echo "Retrieving kitchen inventory..."
  response=$(curl -s "$BASE_URL/kitchen/inventory")
  print_json "$response"
}

# Random Utility Function
get_random_number() {
  echo "Getting random number..."
  response=$(curl -s "$BASE_URL/random")
  print_json "$response"
}

# Battle Leaderboard Function
get_battle_leaderboard() {
  echo "Retrieving battle leaderboard..."
  response=$(curl -s "$BASE_URL/battle/leaderboard")
  print_json "$response"
}

# Start Smoketest Sequence

echo "Starting meal_max smoketest..."

# Initial Health and DB Checks
check_health
check_db

# Meal Management Tests - Adding multiple meals and retrieving them
clear_meals
create_meal '{"name": "Spaghetti", "price": 12.99, "cuisine": "Italian", "difficulty": "MED"}'
create_meal '{"name": "Sushi", "price": 18.99, "cuisine": "Japanese", "difficulty": "HIGH"}'
create_meal '{"name": "Burger", "price": 8.99, "cuisine": "American", "difficulty": "LOW"}'
get_all_meals

# Battle Management Tests - Preparing different combatants and starting battles
clear_battles
prepare_battle '{"meal_id": 1}'
prepare_battle '{"meal_id": 2}'
start_battle
prepare_battle '{"meal_id": 2}'
prepare_battle '{"meal_id": 3}'
start_battle
get_battle_stats

# New Leaderboard Check
get_battle_leaderboard

# Kitchen Management Tests - Updating stats multiple times
update_meal_stats 1 "win"
update_meal_stats 2 "loss"
update_meal_stats 3 "win"
get_kitchen_inventory

# Random Utility Tests - Calling random number multiple times
get_random_number
get_random_number

echo "Meal_max smoketest completed successfully!"