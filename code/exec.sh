for fn in ./DATA/*.graph; do
    echo $fn
    
    python code/main.py -inst ./DATA/email.graph -alg BnB -time 200 -seed 1
    for seed in {1..10}; do
        echo $fn $seed
        python code/main.py -inst $fn -alg APPROX -time 100 -seed $seed
        python code/main.py -inst $fn -alg FASTVC -time 100 -seed $seed
        python code/main.py -inst $fn -alg SA -time 100 -seed $seed
    done 
done