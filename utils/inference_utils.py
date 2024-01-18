import numpy as np

def inference(env, policy,save = True):
    re_list = []
    for ep in range(10):
        ep_steps = 0
        ep_tot_reward = 0
        state = env.reset()
        if save:
            env.store_next_episode()
        while True:
            # samples random action
            action = policy(state)
            # applies action and advances environment by one step
            state, reward, done, info = env.step(action)
            ep_steps += 1
            ep_tot_reward += reward


            # check if done
            
            if done or (ep_steps >= 1000):
                print(
                    f"Episode {ep} ending; steps={ep_steps}; reward={ep_tot_reward:0.3f}; \
                    com={env.model.com_pos()}"
                )
                if save:
                    env.write_now()
                env.reset()
                re_list.append(ep_tot_reward)
                break
        maxs = np.where(re_list==max(re_list))[0][0]
        print(f'Epis: {maxs+1},Max_Re:{re_list[maxs]}')
