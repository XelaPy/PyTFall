init -5 python:
    class BrothelBlock(PrivateBusiness):
        SORTING_ORDER = 5
        COMPATIBILITY = []
        MATERIALS = {"Wood": 70, "Bricks": 30, "Glass": 5}
        NAME = "Brothel"
        IMG = "content/buildings/upgrades/room.jpg"
        DESC = "A place to freck in!"
        def __init__(self, **kwargs):
            super(BrothelBlock, self).__init__(**kwargs)

            self.jobs = set([simple_jobs["Whore Job"]])

        def request_resource(self, client, worker):
            """Requests a room from Sim'Py, under the current code,
               this will not be called if there are no rooms available...
            """
            with self.res.request() as request:
                yield request

                # All is well and the client enters:
                temp = "{}: {} and {} enter the room.".format(self.env.now, client.name, worker.name)
                self.log(temp)

                # This line will make sure code halts here until run_job ran it's course...
                yield self.env.timeout(self.time)
                result = self.run_job(client, worker)

                if result >= 150:
                    line = "The service was excellent!"
                elif result >= 100:
                    line = "The service was good!"
                elif result >= 50:
                    line = "The service was 'meh'."
                else:
                    line = "The service was shit."
                temp = "{} 'did' {}... {}".format(
                            set_font_color(worker.name, "pink"),
                            client.name,
                            line)
                self.log(temp, True)
                temp = "{} leaves the {}.".format(client.name, self.name)
                self.log(temp, True)
                # client.flag("jobs_busy").interrupt()
            client.del_flag("jobs_busy")

        def run_job(self, client, worker):
            """Handles the job and job report.
            """
            # Execute the job/log results/handle finances and etc.:
            job, building = self.job, self.building
            log = NDEvent(job=job, char=worker, loc=building, business=self)

            job.settle_workers_disposition(worker, log)

            difficulty = building.tier
            effectiveness = job.effectiveness(worker, difficulty, log, False)

            # Upgrade mods:
            # Move to Job method?
            eff_mod = 0
            for u in self.upgrades:
                eff_mod += getattr(u, "job_effectiveness_mod", 0)
            effectiveness += eff_mod

            result = job.work_brothel(worker=worker, client=client, building=building,
                                      log=log, effectiveness=effectiveness)

            worker.jobpoints -= job.calc_jp_cost(worker, log,
                        manager_effectiveness=building.manager_effectiveness,
                        cost=100)

            earned = payout(job, effectiveness, difficulty,
                            building, self, worker, client, log)

            # Dirt:
            building.dirt += randint(3, 6)

            # Log everything:
            log.after_job()
            NextDayEvents.append(log)

            # We return the char to the nd list:
            building.available_workers.insert(0, worker)
            return result
